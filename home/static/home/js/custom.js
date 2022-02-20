// search submits form
const searchForm = document.getElementById('search-form');
const searchField = document.getElementById('search-field');

searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (searchField.value !== '' && searchField.value.length > 3) {
        window.location.href = `/search/${searchField.value}/`;
    } else {
        window.location.href = '?humbleMessage=with-all-due-respect-i-just-wanna-say---please-put-some-effort-and-type-minimum-3-characters-long';
    }
});


// subscribe modal
const modal = document.getElementById("subscribe_modal");
const btn = document.getElementById("subscribe_link");
const span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}
span.onclick = function() {
    modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Ask to subscribe
const lastModalPopup = localStorage.getItem('lastModalPopup')
const lastDate = new Date(lastModalPopup);
const today = new Date();

const diffTime = Math.abs(today - lastDate);
const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 

if (lastModalPopup === null || diffDays > 1) {
    setTimeout(() => {
        btn.click()
        localStorage.setItem('lastModalPopup', new Date())
    }, 3000);
}