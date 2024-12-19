
document.addEventListener("DOMContentLoaded", function() {
    const modal = document.querySelector('#loginModal');
     if (modal) {
        modal.style.display = 'none';
    } else {
        console.error("Modal element not found");
    }

    const urlParams = new URLSearchParams(window.location.search)

    if (urlParams.has('showLogin') && urlParams.get('showLogin') === 'true') {
        setTimeout(() => {
            toggleLoginModal();

            if (urlParams.has('formRegistration')) {
                alert('New user registered. Please login to continue.');
            }
        }, 100);
    }
    else{
        console.error("modal not found");
    }
});


function registerClose() {
   
    const registerModal = document.getElementById('registerModal');
    if (registerModal) {
        registerModal.style.display = 'none';
    }
        window.location.href = '/?showLogin=true&fromRegistration=true';  
}

async function toggleLoginModal() {
    const sidebar = document.querySelector('#sidebar-active');
    const modal = document.querySelector('#loginModal');

    if (!modal) {
        console.error("Login modal not found");
        return;
    }

    if (sidebar) {
        sidebar.checked = false;
    }

    const currentDisplay = modal.style.display === 'flex' || getComputedStyle(modal).display === 'flex';
    modal.style.display = currentDisplay ? 'none' : 'flex';
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
        console.log('Login response:', result)

        if (result.success) {

            if(result.redirect) {
                window.location.href = result.redirect;
            }
            else{
               window.location.href = '/main-cont';
            }
        } 
        else {
            alert(result.message || 'Login failed')
        }
    }
    catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
    }
}




async function calculate(event){

    if(event) {
        event.preventDefault();
    }

    const graphContainer = document.getElementById('calc-graph');
    const resultContainer = document.getElementById('calc-result');
    const defaultContent = document.getElementById('default-mage');
    
    if(!graphContainer) {
        console.error("Graph container not found");
        alert("Error: Graph container not found on page");
        return;
    }

    try{

        if(defaultContent){
            defaultContent.style.display = 'none'
        }

        graphContainer.innerHTML = `<p>Loading...</p>`;

        const formData = {
            electricbill: document.getElementById('energy1')?.value.trim() || '0',
            gasbill: document.getElementById('energy2')?.value.trim() || '0',
            fuelbill: document.getElementById('energy3')?.value.trim() || '0',
            wstweight: document.getElementById('waste1')?.value.trim() || '0' ,
            recycled_perc: document.getElementById('waste2')?.value.trim || '0'(),
            distance_traveled: document.getElementById('business1')?.value.trim() || '0',
            fuelef_avg: document.getElementById('business2')?.value.trim() || '0'
        };

        console.log('Sending data:', formData);     

        const response = await fetch('/main-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            credentials: 'same-origin',
            body: JSON.stringify(formData)

        });

        const result = await response.json();
        console.log('Recieved result:', result)

        if(!response.ok) {
            throw new Error(result.error || 'Failed to calculate carbon emission');
        }

        const energyElement = document.getElementById('energy-emission');
        if (energyElement && result.total_carbon_emission_by_energy !== undefined) {
            energyElement.textContent = result.total_carbon_emission_by_energy.toFixed(2);
        }

        const wasteElement = document.getElementById('waste-emission');
        if (wasteElement && result.total_carbon_emission_by_waste !== undefined) {
            wasteElement.textContent = result.total_carbon_emission_by_waste.toFixed(2);
        }

        const businessElement = document.getElementById('business-emission');
        if (businessElement && result.total_carbon_emission_by_business !== undefined) {
            businessElement.textContent = result.total_carbon_emission_by_business.toFixed(2);
        }


        const graphImg = document.getElementById('carbon-graph');
        if (graphImg && result.graph){
            graphImg.src = `data:image/persSignup;base64,${result.graph}`;
            graphContainer.innerHTML = '';
        }


        resultContainer.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
       
    }
    catch (error) {
        console.error('Calculation error:', error);
        graphContainer.innerHTML = `
       <div class="error-message">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12" y2="16" />
                </svg>
                <p>Error: ${error.message}</p>
            </div>
        `;

        if(defaultContent) {
            defaultContent.style.display = 'flex';
        }
    }
}


function handleFormSubmit(event) {
    event.preventDefault();
    calculate(event);
}

