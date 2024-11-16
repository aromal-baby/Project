
document.addEventListener("DOMContentLoaded", function() {
    const modal = document.querySelector('#loginModal');
     if (modal) {
        modal.style.display = 'none';
    } else {
        console.error("Modal element not found");
    }
});


function toggleLoginModal(){
    const sidebar = document.querySelector('#sidebar-active');
    const modal = document.querySelector('#loginModal');

    if(sidebar){
        sidebar.checked = false;
    }

    if (modal.style.display === 'flex'){
        modal.style.display = 'none';
    }
    else{
        modal.style.display = 'flex';
    }
}

function toggleSignup(){

    document.getElementById('modal-content').innerHTML = `
    <div class="modal-content" style="height: 90%;">

        <form style="width:100%">
            <label>
                <input type="radio" name="signup" id="rd-btn" onclick="persSingnup()" checked> Personal
            </label>
            <label>
                <input type="radio" name="signup" onclick="instSignup()"> Institute
            </label>
                <br><br>

                <div id="persdetails">
                    <label for="frstname">First Name</label><br>
                    <input type="text" id="frstrname" required><br><br>
                    <label for="lstname">Last Name</label><br>
                    <input type="text" id="lstname" required><br><br>
                    <label for="ph_num"> Mobile Number</label><br>
                    <input typr="text" id="ph_num"><br><br>
                    <label for="email">E-mal address</label><br>
                    <input type="email" id="emailad" required><br><br>
                    <label for="email">Confirm your E-mail address</label><br>
                    <input type="email" id="emailad" required><br><br>
                    <label for="pass">Enter a password</label><br>
                    <input type="password" id="pass" required><br>
                    <p>Atleast 8 characters, should <br> contain letters,numbers and special characters</p><br>
                    <label for="pass">confirm your password</label><br>
                    <input type="password" id="pass" required><br><br> 
                    <button type="button" id="signup-btn">signUp/Register</button>
                </div>

                <div id="instdetails" style="display:none">
                    <label for="frstname">First Name</label><br>
                    <input type="text" id="frstrname" required><br><br>
                    <label for="lstname">Last Name</label><br>
                    <input type="text" id="lstname" required><br><br>
                    <label for="ph_num"> Mobile Number</label><br>
                    <input typr="text" id="ph_num"><br><br>
                    <label for="postn">Position as </label><br>
                    <input type="text" id="postn"><br><br>
                    <label for="cmpny">Name of the company</label><br>
                    <input type="text" id="cmpny"><br><br>
                    <label for="cmpadrs">Address</label><br>
                    <input type="text" id="cmpadrs"><br><br>
                    <label for="empnum">No. Employees</label><br>
                    <input type="text" id="empnum"><br><br>
                    <label for="email">E-mal address</label><br>
                    <input type="email" id="emailad" required><br><br>
                    <label for="email">Confirm your E-mail address</label><br>
                    <input type="email" id="emailad" required><br><br>
                    <label for="pass">Enter a password</label><br>
                    <input type="password" id="pass" required><br>
                    <p>Atleast 8 characters, should <br> contain letters,numbers and special characters</p><br>
                    <label for="pass">confirm your password</label><br>
                    <input type="password" id="pass" required><br><br> 
                    <button type="button" id="signup-btn">signUp/Register</button>
                </div>
         </form>

        <button id="back-btn" onclick="resetLoginModal()">
            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="black">
                <path d="m313-440 224 224-57 56-320-320 320-320 57 56-224 224h487v80H313Z"/>
            </svg>
        </button>

        <button id="button" onclick="toggleLoginModal()">
            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="black">
                <path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/>
            </svg>
        </button>

    </div>`  
}

function resetLoginModal(){
    document.getElementById('modal-content').innerHTML=`
    <div id="loginModal">
        <div class="modal-content" id="modal-content">
        <div id="loginText">
            <h2>Login</h2>
        </div>
        <div id="loginPort">
            <form>
                <label for="username">Username</label><br>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Password</label><br>
                <input type="password" id="password" name="password" required><br><br>
                <label for=""><input type="checkbox">Remeber Me 
                    <a href="#">Forget password?</a>
                </label>
                <br><br>
                <button id="login-btn" type="submit"  onclick="#">Login</button><br>
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
    </div>`
}

function persSingnup(){
    document.getElementById('persdetails').style.display = 'block';
    document.getElementById('instdetails').style.display = 'none';
}

function instSignup(){
    document.getElementById('persdetails').style.display = 'none';
    document.getElementById('instdetails').style.display = 'block';
}

async function registerUser(){
    const firstName = document.getElementById('frstname').value;
    const lastname = document.getElementById('lstname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('pass').value;

    const response =  await fetch('http://localhost:5000/register',{
        methods: 'POST',
        header: {'content-Type': 'application/json'},
        body: JSON.stringify({firstName, lastName, email, password})
    });

    const result = await response.json();
    alert(result.message || result.error);
}


async function loginUser() {
    const email = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = awit fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'content-Type': 'application/json' },
        body: JSON.stringify({  email, Password})
    });

    const result = await response.json();
    alert(result.message || result.error);
}

