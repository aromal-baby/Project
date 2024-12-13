function toggleLoginModal(){
    const sidebar = document.querySelector('#sidebar-active');
    const modal = document.querySelector('#loginModal');

    if(sidebar){
        sidebar.checked = false;
    }

    if (modal.style.display === 'flex' || getComputedStyle(modal).display === 'flex') { 
        modal.style.display = 'none';
    }
    else{
        modal.style.display = 'flex';
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const modal = document.querySelector('#loginModal');
     if (modal) {
        modal.style.display = 'none';
    } else {
        console.error("Modal element not found");
    }

    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.has('showLogin') && urlParams.get('showLogin') === 'true') {
        toggleLoginModal();
        alert('New user registered. Please login to continue.');
    }
});


function registerClose() {
    // Close the registration modal
    const registerModal = document.getElementById('registerModal');
    if (registerModal) {
        registerModal.style.display = 'none';
    }
        // Redirect to the homepage
        window.location.href = '/?showLogin=true';
    
    
}


function persSignup() {
    document.getElementById('persdetails').style.display = 'block';
    document.getElementById('instdetails').style.display = 'none';
}

function instSignup() {
    document.getElementById('persdetails').style.display = 'block';
    document.getElementById('instdetails').style.display = 'block';
}


function resetLoginModal(){
    document.getElementById('modal-content').innerHTML=`
    <div id="loginModal">
        <div class="modal-content" id="modal-content">
        <div id="loginText">
            <h2>Login</h2>
        </div>
        <div id="loginPort">
            <form onsubmit="event.preventDefault(); loginUser();">
                <label for="username">Username</label><br>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Password</label><br>
                <input type="password" id="password" name="password" required><br><br>
                <label for=""><input type="checkbox">Remeber Me 
                    <a href="#">Forget password?</a>
                </label>
                <br><br>
                <button id="login-btn" type="submit">Login</button><br>
                <center><p>Don't have an account <a href="#" onclick="toggleSignup()">Register?</a></p></center>
                </form>
                <button id="button" onclick="toggleLoginModal()">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="black">
                        <path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/>
                    </svg>
                </button>
            </form>
        </div>
        </div>
    </div>`;
}


async function registerUser() {
    const userType = document.querySelector('input[name="signup"]:checked')?.value;
    
    
    const formData = {
        frstname: document.getElementById('frstname')?.value.trim(),
        lstname: document.getElementById('lstname')?.value.trim(),
        phone: document.getElementById('phone')?.value.trim(),
        email: document.getElementById('email')?.value.trim(),
        password: document.getElementById('Regpassword')?.value.trim(),
        cnfpass: document.getElementById('cnfpass')?.value.trim(),
        userType: userType
    };


    // Additional fields for INSTITUTE type
    if (userType === 'INSTITUTE') {
        formData.postn = document.getElementById('postn')?.value.trim();
        formData.cmpny = document.getElementById('cmpny')?.value.trim();
        formData.adrs = document.getElementById('adrs')?.value.trim();
        formData.empnum = document.getElementById('empnum')?.value.trim();
    }

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        }); 

        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);


        if(!response.ok) {
            const errorText = await response.text();
            console.error('Error response text:', errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        } 

        const result = await response.json();

        if(result.success) {
            alert(result.flashMessage || 'Regitration successful')

            window.location.href = '/?showLogin=true';
        }
        else {
            alert('Registration failed');
        }
    } 
    catch (error) {
        console.error('Full Error during registration:', error);

        if(error instanceof SyntaxError) {
            alert('Server response could not be passed. Please check the server logs.');
        }
        else {
            alert('An error occurred during registration:');  
        }
        
    }
}


async function loginUser() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const rememberMe = document.querySelector('input[type="checkbox"]').checked;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password,
                rememberMe
            })
        });

        const result = await response.json();

        if (response.ok) {
            
            alert('Login successful');
            window.location.href = '/main-content';
        } else {
            
            alert(result.errorMessage || 'Login failed. Please check your credentials.');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
    }
}

async function calculate(){
    
}