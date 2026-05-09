document.addEventListener("DOMContentLoaded", function () {
    const btnEscuro = document.getElementById("btn-tema-escuro");
    const btnClaro = document.getElementById("btn-tema-claro");

    //aplica o tema salvo em qualquer página
    if (localStorage.getItem("tema") === "escuro") {
        document.body.classList.add("tema-escuro");
    }

    //ativa tema escuro
    if (btnEscuro) {
        btnEscuro.addEventListener("click", function () {
            document.body.classList.add("tema-escuro");
            localStorage.setItem("tema", "escuro");
        });
    }

    //ativa tema claro
    if (btnClaro) {
        btnClaro.addEventListener("click", function () {
            document.body.classList.remove("tema-escuro");
            localStorage.setItem("tema", "claro");
        });
    }
});