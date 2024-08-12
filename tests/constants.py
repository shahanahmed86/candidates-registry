signup_data = {
    "email": "pytest@domain.com",
    "password": "123Abc456",
    "first_name": "pytest-first",
    "last_name": "pytest-last",
    "gender": "female",
    "phone": "+923331234563",
}

login_data = {"email": signup_data["email"], "password": signup_data["password"]}

insert_candidate = {
    "email": "candidate-pytest@domain.com",
    "first_name": "candidate-first-name",
    "last_name": "candidate-last-name",
    "gender": "male",
    "phone": "+923331234567",
    "current_job": "MERN Stack Developer",
    "current_employer": "Agilelan Ltd",
    "applied_for": "Gin Backend Developer",
}

update_candidate = {
    "email": "candidate-pytest@domain.com",
    "first_name": "candidate-first-name-update",
    "last_name": "candidate-last-name-update",
    "gender": "female",
    "phone": "+923337654321",
    "current_job": "GIN Backend",
    "current_employer": "Apify Pvt Ltd",
    "applied_for": "FastAPI Backend Developer",
}
