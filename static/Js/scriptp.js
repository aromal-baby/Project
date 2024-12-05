
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
function toggleSignup() {
    document.getElementById('modal-content').innerHTML = `
    <div class="modal-content" style="height: 90%;">

        <form style="width:100%">
            <label>
                <input type="radio" id = "radio-btn" name="signup" value="PERSONAL" onclick="persSignup()" checked> Personal
            </label>
            <label>
                <input type="radio" id = "radio-btn" name="signup" value="INSTITUTE" onclick="instSignup()"> Institute
            </label>
            <br><br>

            <div id="persdetails">
                <label for="frstname">First Name</label><br>
                <input type="text" id="frstname" required><br><br>
                <label for="lstname">Last Name</label><br>
                <input type="text" id="lstname" required><br><br>
                <label for="phone">Mobile Number</label><br>
                <input type="text" id="phone"><br><br>
                <label for="email">E-mail address</label><br>
                <input type="email" id="email" required><br><br>
                <label for="password">Enter a password</label><br>
                <input type="password" id="password" required><br>
                <p>At least 8 characters, should contain letters, numbers, and special characters</p><br>
                <label for="cnfpass">Confirm your password</label><br>
                <input type="password" id="cnfpass" required><br><br> 
                <button type="button" id="pers-signup-btn" onclick="registerUser()">Sign Up/Register</button>
            </div>

            <div id="instdetails" style="display:none;">
                <label for="postn">Position as</label><br>
                <input type="text" id="postn"><br><br>
                <label for="cmpny">Name of the company</label><br>
                <input type="text" id="cmpny"><br><br>
                <label for="adrs">Company Address</label><br>
                <input type="text" id="adrs"><br><br>
                <label for="empnum">Number of Employees</label><br>
                <input type="text" id="empnum"><br><br>
                <label for="password">Enter a password</label><br>
                <input type="password" id="password" required><br>
                <label for="cnfpass">Confirm your password</label><br>
                <input type="password" id="cnfpass" required><br><br>
                <button type="button" id="inst-signup-btn" onclick="registerUser()">Sign Up/Register</button>

            </div>
        </form>
    </div>`;
}

function persSignup() {
    document.getElementById('persdetails').style.display = 'block';
    document.getElementById('instdetails').style.display = 'none';
}

function instSignup() {
    document.getElementById('pers-signup-btn').style.display = 'none';
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
    </div>`;
}

async function registerUser() {
    let firstName, lastName, email, password, phone, position, company, address, employeeCount, userType;
    
    const selectedSignupType = document.querySelector('input[name="signup"]:checked');
    if(selectedSignupType) {
        userType = selectedSignupType.value;
    } else {
        alert("please select a signup type.");
        return;
    }
    
    if (userType === 'PERSONAL') {
        firstName = document.getElementById('frstname').value.trim();
        lastName = document.getElementById('lstname').value.trim();
        email = document.getElementById('email').value.trim();
        phone = document.getElementById('phone').value.trim();
        password = document.getElementById('password').value.trim();
    
    
        const confirmPass = document.getElementById('cnfpass').value.trim();
        if(password !== confirmPass) {
            alert('Passwords do not match');
            return;
        }
    
    } 
    
    else if (userType === 'INSTITUTE') {
        firstName = document.getElementById('frstrname').value.trim();
        lastName = document.getElementById('lstname').value.trim();
        phone = document.getElementById('phone').value.trim();
        email = document.getElementById('email').value.trim();
        password = document.getElementById('pass').value.trim();
        position = document.getElementById('postn').value.trim();
        company = document.getElementById('cmpny').value.trim();
        address = document.getElementById('adrs').value.trim();
        employeeCount = document.getElementById('empnum').value.trim();
    

        const confirmPass = document.getElementById('cnfpass').value.trim();
        if(password !== confirmPass ) {
            alert('Passwords mismatch');
            return;
        }
    } 


    try{
        const response = await fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                frstname: firstName,
                lstname: lastName,
                phone: phone,
                email: email,
                pass: password,
                position: position || null,
                company: company || null,
                address: address || null,
                employeeCount: employeeCount || null,
                userType
            }),
        });
    
        const result = await response.json();
        if (response.ok) {
            alert(result.message)
        }
        else {
            alert(result.message || result.error);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occured during registration.');
    }
}


async function loginUser() {
    const email = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const respomse = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({email, password})
        });

        const result = await response.json();
        if(response.ok) {
            alert(result.message);

            if(result.userType === 'PERSONAL') {
                window.location.href = '/personal-dashboard';
            } else if (result.userType === 'INSTITUTE'){
                window.location.href = '/institute-dashboard';
            }
        }else {
            alert(result,error);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occured during login.');
    }
}


function toggleAboutUsModal() {
    var modal = document.getElementById('aboutUsModal');
    if(modal.display === 'flex') {
        modal.style.display = 'none';
    } else {
        modal.style.display = 'flex';
    }
}