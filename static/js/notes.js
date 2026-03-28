document.querySelectorAll(".edit-btn").forEach(button => {
  button.addEventListener("click", function () {

    const card = this.closest(".card-body")

    const text = card.querySelector(".note-text")
    const form = card.querySelector(".edit-form")

    text.style.display = "none"
    form.style.display = "block"
    this.style.display = "none"

  })
})