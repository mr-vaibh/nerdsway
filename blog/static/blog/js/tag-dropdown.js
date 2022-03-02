// ====== Tags Dropdown ======
let tagsList;

const updateTagList = () => {
    tagsList = tagsInput.value.split(',')
                .map(item => item.trim())
                .filter(item => item !== '')
    
    tagPills.innerHTML = ''
    tagsList.map(tag => {
        tagPills.innerHTML += `<span class="pill">${tag} <span class="remove" onclick="removeTag('${tag}');">&times;</span></span>`
    })
    addTagInput.value = ''
}
const addTag = (tag) => {
    tagsInput.value += `${tag}, `
    updateTagList()
}
const removeTag = (tag) => {
    tagsInput.value = tagsInput.value.replaceAll(tag, '')
    updateTagList()
}

updateTagList()


// Suggestion Box show and hide logic
addTagInput.addEventListener('input', (e) => {
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
    const searched_tag = e.target.value;
    fetch(`/tag/search/${searched_tag}/`)
        .then(response => response.json())
        .then(data => {
            tagSuggestions.children[0].innerHTML = ''
            
            if (data['suggestions'].length > 0) {
                data['suggestions'].map(tag => {
                    tagSuggestions.children[0].innerHTML += `<span onclick="addTag('${tag}');">${tag}</span>`
                })
            } else {
                tagSuggestions.children[0].innerHTML = `No tags were found. <span onclick="addTag('${searched_tag}');">Create a tag <b>${searched_tag}</b></span>`
            }
        })
        .catch(error => console.error(error))
})