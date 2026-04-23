# importa exceção de validação do django
from django.core.exceptions import ValidationError

from django.db.models import Q

# importa o modelo de usuário
from apps.usuarios.models import Usuario

# classe responsável por centralizar regras de negócio do usuário
class UsuarioService:

    # método para criar usuário
    @staticmethod
    def criar_usuario(data: dict) -> Usuario:
        # pega a senha do dicionário
        password = data.pop("password", None)

        # valida se a senha foi informada
        if not password:
            raise ValidationError("senha é obrigatória.")

        # cria usuário usando o método padrão do django
        user = Usuario.objects.create_user(password=password, **data)

        # retorna o usuário criado
        return user

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
        # define os campos que podem ser alterados
        campos_permitidos = ["first_name", "last_name", "email", "telefone", "foto"]

        # percorre os campos permitidos
        for campo in campos_permitidos:
            # verifica se o campo está nos dados enviados
            if campo in data:
                # atualiza o valor do campo
                setattr(usuario, campo, data[campo])

        # salva as alterações
        usuario.save()

        # retorna o usuário atualizado
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
        # importa Q para consultas complexas

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
