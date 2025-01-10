function product_visibility(user_type) {
    const product_options = user_type.nextElementSibling;
    if (['Product Owner', 'Tester'].includes(user_type.value)) {
        product_options.style.display = 'block';
    }
    else {
        product_options.style.display = 'none';
    }
}

///////////// default visibility //////////////////
// const unapproved_users = document.querySelector('#unapproved');
const all_user_types = document.querySelectorAll('#user-type');
all_user_types.forEach(user_type => {
    user_type_option = user_type.querySelector('#User-type-options');
    if (!['Product Owner', 'Tester'].includes(user_type_option.value)) {
        const product_options = user_type_option.nextElementSibling;
        product_options.style.display = 'none';
    }
});
/////////////////////////////////////////////////

function get_new_data(button){
    const user_row = button.parentElement.parentElement.parentElement;
    const userType = user_row.querySelector('#User-type-options');
    let user_type;
    if (userType.value === 'Product Owner') {
        user_type = 'owner';
    } else if (userType.value === 'Tester') {
        user_type = 'employee';
    } else if (userType.value === 'Brand') {
        user_type = 'brand';
    } else if (userType.value === 'Legal') {
        user_type = 'legal';
    } else {
        user_type = userType.value;
    }

    let productTypes = [];
    if (['owner', 'employee'].includes(user_type)) {
        const productTypeDiv = user_row.querySelector('#Product-type-options');
        const ProductTypeSpans = productTypeDiv.querySelectorAll('.multi-select-header-option');

        ProductTypeSpans.forEach(productTypeValue => {
            let productType = productTypeValue.textContent.trim();
            productTypes.push(productType);
        });
    }
    return {user_type, productTypes};
}

function callDjango(url, user_type, productTypes, username) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            userType: user_type,
            productTypes: productTypes
        })
    })

    .then(response => {
        if (response.ok) {
            location.reload();
        }
        else {console.error('Request failed with status:', response.status);}
    })
    .catch(error => {console.error('Error:', error);});
}

function approveUser(button, username) {
    let new_data = get_new_data(button);
    let user_type = new_data.user_type;
    let productTypes = new_data.productTypes;
    
    if (user_type === "Select User Type") {alert("Please select a User Type to approve the user.");}
    else{
        callDjango('/au/approveUser/', user_type, productTypes, username)
    }
}

function updateUser(button, username) {
    let new_data = get_new_data(button);
    let user_type = new_data.user_type;
    let productTypes = new_data.productTypes;

    callDjango('/au/updateUser/', user_type, productTypes, username);
}

function removeUser(removal_type, button, username) {
    let new_data = get_new_data(button);
    let user_type = new_data.user_type;
    let productTypes = new_data.productTypes;

    callDjango(`/au/removeUser/${removal_type}`, user_type, productTypes, username);
}