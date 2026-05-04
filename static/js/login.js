//validar
if (!email || !senha) {
  Swal.fire({
    icon: "error",
    title: "Campos obrigatórios",
    text: "Preencha email e senha corretamente"
  });
  return;
}

//login (sucesso e erro)
fetch("/api/login/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ email, senha })
})
.then(async res => {
  const data = await res.json(); //pega mensagem do backend

  if (res.ok) {
    Swal.fire({
      icon: "success",
      title: "Login realizado!",
      text: "Bem-vindo!"
    }).then(() => {
      window.location.href = "mapa.html";
    });
  } else {
    Swal.fire({
      icon: "error",
      title: "Erro no login",
      text: data.mensagem || "Email ou senha incorretos"
    });
  }
});