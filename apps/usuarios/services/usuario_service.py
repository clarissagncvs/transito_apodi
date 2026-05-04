import random
from datetime import timedelta

# importa exceção de validação do django
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.shortcuts import get_object_or_404

# importa o modelo de usuário
from apps.usuarios.models import Usuario


# classe responsável por centralizar regras de negócio do usuário
class UsuarioService:

    # método para criar usuário
    @staticmethod
    def criar_usuario(data: dict) -> Usuario:
        # Tenta pegar password1 (do form) ou password (da sessão/teste)
        password = data.pop("password1", data.pop("password", None))
        password_confirm = data.pop("password2", password)  # Se não houver p2, assume igual

        if not password:
            raise ValidationError("senha é obrigatória.")

        if password != password_confirm:
            raise ValidationError("as senhas não coincidem.")

        # Se a View não mandou o status, o padrão é False
        if "is_active" not in data:
            data["is_active"] = False

        user = Usuario.objects.create_user(
            password=password,
            **data
        )

        # Só envia e-mail se o usuário for criado inativo
        if not user.is_active:
            UsuarioService.gerar_e_enviar_codigo(user)

        return user

    # método para gerar código e enviar e-mail
    @staticmethod
    def gerar_e_enviar_codigo(usuario: Usuario):
        # gera código de 6 dígitos
        codigo = str(random.randint(100000, 999999))

        # salva no usuário com expiração de 10 min
        usuario.codigo_verificacao = codigo
        usuario.codigo_expira_em = timezone.now() + timedelta(minutes=10)
        usuario.is_active = False

        # salva os novos campos no banco de dados
        usuario.save(
            update_fields=["codigo_verificacao", "codigo_expira_em", "is_active"]
        )

        # dispara o e-mail
        send_mail(
            subject="🚗 Ativação de Conta - Trânsito Apodi",
            message=(
                f"Olá, {usuario.username}!\n\n"
                f"Bem-vindo ao sistema de monitoramento de trânsito de Apodi!\n"
                f"Seu código de segurança é: {codigo}\n\n"
                f"Insira este código no site para ativar sua conta. "
                f"Ele será válido por apenas 10 minutos."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,  # lembre-se de configurar no settings.py
            recipient_list=[usuario.email],
            fail_silently=False,
        )

    @staticmethod
    def reenviar_codigo(usuario):
        # gera novo código de 6 dígitos
        novo_codigo = get_random_string(
            length=6,
            allowed_chars='0123456789'
        )

        # atualiza o código e o prazo — 10 minutos
        usuario.codigo_verificacao = novo_codigo
        usuario.codigo_expira_em = timezone.now() + timedelta(minutes=10)
        usuario.save(update_fields=[
            'codigo_verificacao',
            'codigo_expira_em'
        ])

        # envia o e-mail
        send_mail(
            subject='Novo código — Trânsito Apodi',
            message=f'Seu novo código é: {novo_codigo}\n\nExpira em 10 minutos.',
            from_email=None,
            recipient_list=[usuario.email],
            fail_silently=False,
        )

    # método para alterar o tipo do usuário
    @staticmethod
    def alterar_tipo(
        usuario: Usuario, novo_tipo: str, usuario_logado: Usuario = None
    ) -> Usuario:
        # valida se o tipo é válido
        if novo_tipo not in Usuario.Tipo.values:
            raise ValidationError("tipo inválido.")

        # impede que o admin remova o próprio acesso
        if usuario_logado and usuario == usuario_logado:
            if novo_tipo != Usuario.Tipo.ADMIN:
                raise ValidationError(
                    "você não pode remover seu próprio acesso de admin."
                )

        # altera o tipo do usuário
        usuario.tipo = novo_tipo

        # salva apenas o campo alterado
        usuario.save(update_fields=["tipo"])

        # retorna o usuário atualizado
        return usuario

    # método para ativar ou desativar usuário
    @staticmethod
    def toggle_ativo(usuario: Usuario, usuario_logado: Usuario = None) -> Usuario:
        # impede que o usuário desative a própria conta
        if usuario_logado and usuario == usuario_logado:
            raise ValidationError("você não pode desativar sua própria conta.")

        # alterna o status ativo
        usuario.is_active = not usuario.is_active

        # salva apenas o campo alterado
        usuario.save(update_fields=["is_active"])

        # retorna o usuário atualizado
        return usuario

    # método para atualizar perfil
    @staticmethod
    def atualizar_perfil(usuario: Usuario, data: dict) -> Usuario:
        # Percorre os dados validados e aplica ao objeto
        for campo, valor in data.items():
            setattr(usuario, campo, valor)

        usuario.save()
        return usuario

    # método para deletar usuário
    @staticmethod
    def deletar_usuario(usuario: Usuario, usuario_logado: Usuario = None):
        # impede que o usuário delete a própria conta
        if usuario_logado and usuario == usuario_logado:
            raise ValidationError("você não pode deletar sua própria conta.")

        # deleta o usuário
        usuario.delete()

    # método para filtrar usuários
    @staticmethod
    def filtrar_usuarios(qs, tipo=None, busca=None, ativo=None):
        # filtra por tipo
        if tipo:
            qs = qs.filter(tipo=tipo)

        # filtra por busca em múltiplos campos
        if busca:
            qs = qs.filter(
                Q(username__icontains=busca)
                | Q(first_name__icontains=busca)
                | Q(email__icontains=busca)
            )

        # filtra por status ativo
        if ativo == "1":
            qs = qs.filter(is_active=True)
        elif ativo == "0":
            qs = qs.filter(is_active=False)

        # retorna queryset filtrado
        return qs

#  métodos de ativação e solicitação
    @staticmethod
    def ativar_conta_por_codigo(usuario_id, codigo_digitado):
        """Valida o código e ativa o usuário."""
        usuario = get_object_or_404(Usuario, id=usuario_id)
        agora = timezone.now()

        if usuario.codigo_verificacao == codigo_digitado and usuario.codigo_expira_em > agora:
            usuario.is_active = True
            usuario.codigo_verificacao = None
            usuario.save(update_fields=['is_active', 'codigo_verificacao'])
            return usuario
        raise ValidationError("Código inválido ou expirado.")

    @staticmethod
    def solicitar_upgrade_tipo(usuario, novo_tipo, absolute_uri):
        """
        Envia a solicitação DIRETAMENTE para o e-mail do sistema (configurado no .env).
        """
        # 1. Configura o assunto com o tipo escolhido (AGENTE ou ADMIN)
        assunto = f"[{novo_tipo}] Solicitação de Mudança de Conta - {usuario.username}"

        # 2. Monta a mensagem detalhada
        mensagem = f"""
        Nova solicitação de alteração de nível de acesso no sistema Trânsito Apodi.

        DADOS DO SOLICITANTE:
        ---------------------------------
        Usuário: {usuario.username}
        E-mail do usuário: {usuario.email}
        Nível Atual: {usuario.get_tipo_display()}
        MUDANÇA SOLICITADA PARA: {novo_tipo}  <--

        AÇÃO NECESSÁRIA:
        Para aprovar ou alterar o perfil deste usuário, acesse o link:
        {absolute_uri}
        """

        # 3. Define o destinatário como o e-mail do próprio sistema (seu .env)
        # O destinatário será o valor de DEFAULT_FROM_EMAIL
        destinatarios = [settings.DEFAULT_FROM_EMAIL]

        # 4. Disparo obrigatório
        try:
            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=destinatarios,
                fail_silently=False,  # Garante que erros apareçam no seu terminal
            )
            print(f"✅ E-mail enviado com sucesso para {settings.DEFAULT_FROM_EMAIL}")
        except Exception as e:
            print(f"❌ Falha ao enviar e-mail: {e}")
            raise e
#  Busca Binária

    @staticmethod
    def buscar_usuarios_binario(termo_busca):  # Renomeado para coincidir com o erro do teste
        """Implementação da busca binária para encontrar um usuário específico."""
        if not termo_busca:
            return Usuario.objects.all().order_by('username')

        # Pegamos todos ordenados para a busca binária funcionar
        usuarios_lista = list(Usuario.objects.all().order_by('username'))

        baixo = 0
        alto = len(usuarios_lista) - 1
        alvo = termo_busca.lower()

        while baixo <= alto:
            meio = (baixo + alto) // 2
            chute = usuarios_lista[meio].username.lower()

            if chute == alvo:
                return [usuarios_lista[meio]]

            if chute > alvo:
                alto = meio - 1
            else:
                baixo = meio + 1
        return []
