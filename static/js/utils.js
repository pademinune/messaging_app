
function refresh_page() {
    location.reload();
}

function redirect(url) {
    window.location.href = url;
}

function goBack() {
    window.history.back();
}

function toggle(id) {
    let element = document.getElementById(id)
    
    element.classList.toggle("hidden")
}

