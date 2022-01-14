console.log('inside fetch example');

function getUsers(user_id){
    console.log(user_id);
    fetch(`https://reqres.in/api/users/${user_id}`).then(
        response => response.json()
    ).then(
        response_obj => put_users_inside_html(response_obj.data)
    ).catch(
        err => console.log(err)
    )
}

function put_users_inside_html(response_obj_data) {
    console.log(response_obj_data);
    const curr_main = document.querySelector("main");
    let user = response_obj_data
    const section = document.createElement('section');
    section.innerHTML = `
    <img src="${user.avatar}" alt="Profile Picture"/>
    <div>
        <span>${user.first_name} ${user.last_name}</span>
        <br>
        <a href="mailto:${user.email}">Send Email</a>
    </div>
    `;
    curr_main.appendChild(section);

}