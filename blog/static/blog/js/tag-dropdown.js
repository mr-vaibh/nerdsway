// ====== Tags Dropdown ======
let tagsList;

function updateTagList() {
    tagsList = tagsInput.value.split(',')
                .map(item => item.trim())
                .filter(item => item !== '')
    
    tagPills.innerHTML = ''
    tagsList.map(tag => {
        tagPills.innerHTML += `<span class="pill">${tag} <span class="remove" onclick="removeTag('${tag}');">&times;</span></span>`
    })
    addTagInput.value = ''
}
function addTag(tag) {
    tagsInput.value += `${tag}, `
    updateTagList()
}
function removeTag(tag) {
    tagsInput.value = tagsInput.value.replaceAll(tag, '')
    updateTagList()
}

updateTagList()


// Suggestion Box show and hide logic
addTagInput.addEventListener('input', (e) => {
    console.log(e.target.value.length)
    if (e.target.value.length > 2) {
        tagSuggestions.style.display = 'block';
    } else {
        tagSuggestions.style.display = 'none';
    }
})
document.addEventListener('click', (e) => {
    if (e.target !== tagSuggestions) {
        tagSuggestions.style.display = 'none';
    }
})


// Add tag Search completion logic
addTagInput.addEventListener('input', (e) => {
    fetch(`/tag/search/${e.target.value}/`)
        .then(response => response.json())
        .then(data => {
            tagSuggestions.children[0].innerHTML = ''
            
            if (data['suggestions'].length > 0) {
                data['suggestions'].map(tag => {
                    tagSuggestions.children[0].innerHTML += `<span onclick="addTag('${tag}');">${tag}</span>`
                })
            } else {
                tagSuggestions.children[0].innerHTML = `No tags found. But it will be created anyway.`
            }
        })
        .catch(error => console.error(error))
})