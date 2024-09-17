const form = document.getElementById("form");
const container = document.querySelector(".container");
let formIsValid = false;

form.addEventListener("submit", (e) => {
  e.preventDefault();

  checkInputs();

  if (formIsValid) {
    // Alterar o conteúdo do container para a mensagem de sucesso
    container.innerHTML = `
    <div class="mensagem-sucesso" style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 50px;
        background-color: #e8f5e9;
        border: 2px solid #4caf50;
        border-radius: 15px;
        text-align: center;
        color: #2e7d32;
      ">
        <i class="fas fa-check-circle" style="font-size: 50px; color: #4caf50; margin-bottom: 20px;"></i>
        <h2 style="font-family: 'Poppins', sans-serif; font-size: 28px; font-weight: bold; margin-bottom: 10px;">
          Candidatura Efetuada com Sucesso!
        </h2>
        <p style="font-family: 'Poppins', sans-serif; font-size: 18px; margin-bottom: 20px;">
          Agradecemos pela sua candidatura. Em breve entraremos em contacto.
        </p>
      </div>
    `;

    // Redirecionar para a página principal após 3 segundos
    setTimeout(() => {
      window.location.href = "/";
    }, 5000);
  }
});

function checkInputs() {
  const username = document.getElementById("username");
  const email = document.getElementById("email");
  const telefone = document.getElementById("telefone");
  const nacionalidade = document.getElementById("nacionalidade");
  const areaConcorre = document.getElementById("area-concorre");
  const CV = document.getElementById("CV");

  // Inicializar como válido
  formIsValid = true;

  if (username.value === "") {
    setErrorFor(username, "O nome completo é obrigatório.");
    formIsValid = false;
  } else {
    setSuccessFor(username);
  }

  if (email.value === "") {
    setErrorFor(email, "O email é obrigatório.");
    formIsValid = false;
  } else if (!checkEmail(email.value)) {
    setErrorFor(email, "Por favor, insira um email válido.");
    formIsValid = false;
  } else {
    setSuccessFor(email);
  }

  if (telefone.value === "") {
    setErrorFor(telefone, "O número de telefone é obrigatório.");
    formIsValid = false;
  } else {
    setSuccessFor(telefone);
  }

  if (nacionalidade.value === "") {
    setErrorFor(nacionalidade, "A sua nacionalidade é obrigatória.");
    formIsValid = false;
  } else {
    setSuccessFor(nacionalidade);
  }

  if (areaConcorre.value === "") {
    setErrorFor(areaConcorre, "A área que concorre é obrigatória.");
    formIsValid = false;
  } else {
    setSuccessFor(areaConcorre);
  }

  if (CV.value === "") {
    setErrorFor(CV, "O seu currículo é obrigatório.");
    formIsValid = false;
  } else {
    setSuccessFor(CV);
  }
}

function setErrorFor(input, message) {
  const formControl = input.parentElement;
  const small = formControl.querySelector("small");
  small.innerText = message;
  formControl.className = "form-control error";
}

function setSuccessFor(input) {
  const formControl = input.parentElement;
  formControl.className = "form-control success";
}

function checkEmail(email) {
  return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
    email
  );
}
