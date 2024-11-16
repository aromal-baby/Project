const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql');
const cors = require('cors');

const app = express();
const port = 3306;


const db = mysql.createConnection({
    host: 'loclahost',
    user: 'root',
    password: 'root',
    database: 'crbnftprnt_db'
});

db.connect(err => {
    if (err){
        console.error('database connection error:' err);
    }
    else {
        comnsole.log('Database connected');
    }
});

app.use(cors());
app.use(bodyParser.json());


app.post('?register', async (req, res) => {
  const { fistName, lastName, email, phone, password, position, company, address, employeecount } = req.body;

  try {
    const hashedPassword = await bcrypt.hash(password, 10);

    const query = `
        INSERT INTO users (first_name, last_name, phone, email, password_hash, position_inst, company_name, address, no_employees)
        values (?, ?, ?, ?, ?, ?,?, ?, ?)
    `;
    db.query()
  }
});

db.query(
    query,
    [firstName, lastName, phone, email, hashedPassword, position_inst, company_name, address, no_employees],
    (err, results) => {
        if(err) {
            console.error('Error inserting into databse')
        }
    }
)