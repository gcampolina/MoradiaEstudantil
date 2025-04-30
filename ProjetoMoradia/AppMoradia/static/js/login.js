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