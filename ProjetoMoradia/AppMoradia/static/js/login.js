    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');

    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });

    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });

    

    document.addEventListener('DOMContentLoaded', function () {
        const showLoginBtn = document.getElementById('showLoginBtn');
        const showSignupBtn = document.getElementById('showSignupBtn');
        const signInContainer = document.getElementById('sign-in-container');
        const signUpContainer = document.getElementById('sign-up-container');
        
        if (showLoginBtn && showSignupBtn && signInContainer && signUpContainer) {
            // Botão para mostrar o formulário de login
            showLoginBtn.addEventListener('click', function () {
                signInContainer.style.display = 'block';  // Exibe o login
                signUpContainer.style.display = 'none';   // Oculta o cadastro
            });
    
            // Botão para mostrar o formulário de cadastro
            showSignupBtn.addEventListener('click', function () {
                signUpContainer.style.display = 'block';  // Exibe o cadastro
                signInContainer.style.display = 'none';   // Oculta o login
            });
        } else {
            console.error('Elementos não encontrados!');
        }
    });




// Mascara para o campo de telefone
    const telefone = document.getElementById('telefone');

    telefone.addEventListener('input', function (e) {
      let valor = e.target.value.replace(/\D/g, ''); // Remove não-números
  
      // Limita a 11 dígitos (2 DDD + 9 número de celular)
      valor = valor.slice(0, 11);
  
      if (valor.length >= 1) {
        valor = valor.replace(/^(\d{0,2})/, '($1');
      }
      if (valor.length >= 3) {
        valor = valor.replace(/^(\(\d{2})(\d)/, '$1) $2');
      }
      if (valor.length >= 10) {
        valor = valor.replace(/(\d{5})(\d{4})$/, '$1-$2');
      }
  
      e.target.value = valor;
    });

