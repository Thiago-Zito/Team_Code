document.addEventListener("DOMContentLoaded", async () => {
  const contador = document.getElementById("contador-carrinho");
  const carrinhoIcon = document.querySelector(".carrinho-icon");

  if (!contador || !carrinhoIcon) return;

  try {
    const resposta = await fetch("/api/contador-carrinho");
    const dados = await resposta.json();
    const quantidade = dados.quantidade || 0;

    contador.textContent = quantidade;

    // ⚡ Animação suave no número (badge)
    contador.style.transition = "transform 0.4s ease, background 0.4s";
    contador.style.transform = "scale(1.3)";
    contador.style.background = "#ffc107";

    setTimeout(() => {
      contador.style.transform = "scale(1)";
      contador.style.background = "#ff4747";
    }, 400);

    // 🛒 Animação no ícone
    carrinhoIcon.style.transition = "transform 0.4s ease";
    carrinhoIcon.style.transform = "rotate(-15deg)";
    setTimeout(() => (carrinhoIcon.style.transform = "rotate(0deg)"), 400);

  } catch (error) {
    console.error("Erro ao buscar contador do carrinho:", error);
  }
});
