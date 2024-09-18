const textarea = document.querySelector('.add-comment');
textarea.addEventListener('input', () => {
    textarea.style = 'max-height: 200px';
    textarea.style.height = `${textarea.scrollHeight+2}px`;
});

function toggleRemarks() {
    var remarksSection = document.getElementById('remarks-section');
    var toggleButton = document.getElementById('toggleRemarksBtn');
    const formContainer = document.querySelector('.form-container');
    const ww = window.innerWidth;

    if (remarksSection.classList.contains('visible')) {
        remarksSection.classList.remove('visible');
        if(ww > 1050){
            formContainer.style.right = `0px`;
        }
        toggleButton.style.display = 'flex';
    } else {
        remarksSection.classList.add('visible');
        if(ww > 1050){
            const sw = 350-(ww-700)/2;
            const cw = ww-1050;
            formContainer.style.right = `${sw+cw/2}px`;
            console.log(ww, sw, cw);
        }
        toggleButton.style.display = 'none';
    }
}

function generateRandomString(length) {
    const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let randomString = '';
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        randomString += characters.charAt(randomIndex);
    }
    return randomString;
}

function popupAction(test, action) {
    var remarksSection = document.getElementById('remarks-section');
    if (!remarksSection.classList.contains('visible')) {
        remarksSection.classList.add('visible');
    }
    var popup = document.querySelector('.popup');
    popup.style.display = 'none';
    var selection = window.getSelection();
    var range = selection.getRangeAt(0);
    var div = document.createElement('div');
    div.classList.add("remark");
    div.classList.add(action);
    var dataCommentId = generateRandomString(6);
    div.setAttribute("data-comment-id", dataCommentId);
    range.surroundContents(div);
    createCommentBox(test, dataCommentId, action, '');
    makeRemarkChanges(test, dataCommentId, action, '');
    selection.removeAllRanges();
}

function findCommonParentTag(selection) {
    let currentNode = selection.anchorNode;
    while (currentNode) {
        if (currentNode.contains(selection.focusNode)) {
            return currentNode.parentElement;
        }
        currentNode = currentNode.parentNode;
    }
    return null;
}

let lastSelected = '';
const form = document.querySelector('form'); 
form.addEventListener('mouseup', function(event) {
    var selection = window.getSelection();
    var parentTag = findCommonParentTag(selection).tagName;
    let currSelected = selection.toString();
    validTagList = ['TD', 'SPAN', 'P'];
    if (currSelected !== '' && currSelected !== lastSelected && validTagList.includes(parentTag)) {
        lastSelected = currSelected;
        var popup = document.querySelector('.popup');
        popup.style.display = 'flex';
        popup.style.position = 'absolute';

        var updatePopupPosition = function() {
            var rect = window.getSelection().getRangeAt(0).getBoundingClientRect();
            popup.style.left = rect.left + 'px';
            popup.style.top = rect.top + window.scrollY- 35 + 'px';
        };
        updatePopupPosition();
        window.addEventListener('scroll', updatePopupPosition);
        
        const docListener = function(event) {
            event.stopPropagation();
            if (!popup.contains(event.target)) {
                popup.style.display = 'none';
                window.removeEventListener('scroll', updatePopupPosition);
                document.removeEventListener('mousedown', docListener);
            }
        };
        document.addEventListener('mousedown', docListener);
    }
});

function addCommentBoxListeners() {
    const commentBoxes = document.querySelectorAll('.comment-box');
    commentBoxes.forEach(box => {
        box.addEventListener('mouseenter', function() {
            const commentId = box.id;
            const targetContent = document.querySelector(`[data-comment-id='${commentId}']`);
            if (targetContent) {
                targetContent.classList.add('add-border');
            }
        });
        box.addEventListener('mouseleave', function() {
            const commentId = box.id;
            const targetContent = document.querySelector(`[data-comment-id='${commentId}']`);
            if (targetContent) {
                targetContent.classList.remove('add-border');
            }
        });
    });
}
addCommentBoxListeners();

function handleCommentClick(commentBoxes) {
    // const commentBoxes = document.querySelectorAll('.comment-box');
    commentBoxes.forEach(box => {
        const commentFrom = box.querySelector('.comment-header .comment-from');
        const employeeName = employee_name;
        if (commentFrom.textContent.trim() === employeeName) {
            box.addEventListener('click', function(event) {
                event.stopPropagation();
                const commentContent = box.querySelector('.comment-content');
                const addCommentBox2 = box.querySelector('.add-comment-box-2');
                const textarea = addCommentBox2.querySelector('.comment-content-input');
                if (commentContent) {
                    commentContent.style.display = (commentContent.style.display === 'none') ? 'block' : 'none';
                }
                if (addCommentBox2) {
                    addCommentBox2.style.display = (addCommentBox2.style.display === 'flex') ? 'none' : 'flex';
                    if (addCommentBox2.style.display === 'flex') {
                        textarea.focus();
                        textarea.selectionStart = textarea.value.length;
                        textarea.selectionEnd = textarea.value.length;
                        textarea.style.height = `${textarea.scrollHeight+2}px`;
                        textarea.addEventListener('input', () => {
                        textarea.style = 'max-height: 200px';
                        textarea.style.height = `${textarea.scrollHeight+2}px`;
                        });
                    }
                }
            });
            const addCommentBox2 = box.querySelector('.add-comment-box-2');
            addCommentBox2.addEventListener('click', function(event) {
                event.stopPropagation();
            });
        }
    });
}
handleCommentClick(document.querySelectorAll('.comment-box'));

function addRemarkListeners() {
    const remarkElements = document.querySelectorAll('.remark');
    remarkElements.forEach(remark => {
        const commentId = remark.dataset.commentId;
        const targetContent = document.querySelector(`.comment-box[id='${commentId}']`);
        remark.addEventListener('mouseover', () => {
            const commentId = remark.dataset.commentId;
            remark.style.cursor = 'pointer';
            remark.classList.add('add-border');
            if (targetContent) {
                targetContent.classList.add('add-border');
            }
        });

        remark.addEventListener('mouseout', () => {
            remark.classList.remove('add-border');
            if (targetContent) {
                targetContent.classList.remove('add-border');
            }
        });

        remark.addEventListener('click', () => {
            if (targetContent) {
                const remarksSection = document.querySelector('#remarks-section');
                remarksSection.classList.add('visible');
                // targetContent.focus();
                const commentFrom = targetContent.querySelector('.comment-header .comment-from');
                if (commentFrom.textContent.trim() === employee_name) {
                    const addCommentBox2 = targetContent.querySelector('.add-comment-box-2');
                    addCommentBox2.style.display = 'flex';
                    targetContent.querySelector('.comment-content').style.display = 'none';
                    const textarea = addCommentBox2.querySelector('.comment-content-input');
                    textarea.focus();
                    textarea.selectionStart = textarea.value.length;
                    textarea.selectionEnd = textarea.value.length;
                }
            }
        });
    });
}
addRemarkListeners();

function createCommentBox(test, dataCommentId, type, content) {
    const commentBox = document.createElement('div');
    commentBox.classList.add('comment-box');
    commentBox.id = dataCommentId;

    const commentHeader = document.createElement('div');
    commentHeader.classList.add('comment-header');
    commentBox.appendChild(commentHeader);

    const icon = document.createElement('icon');
    icon.classList.add('comment-icon');
    if (type === "highlight") {
        icon.innerHTML = '<svg height="20px" viewBox="0 -960 960 960" width="20px" fill="#e8eaed"><path d="m548-410-90-91-193 193 91 91 192-193Zm-38-143 90 91 192-192-90-91-192 192Zm-77-24 192 192-218 218q-22 20-50.5 21.5T308-164l-20 20H96l116-116q-21-20-20-49.5t23-49.5l218-218Zm0 0 218-218q21-21 51-21t51 21l90 90q20 22 20 51t-20 51L625-385 433-577Z"/></svg>';
    } else if (type === "underline") {
        icon.innerHTML = '<svg height="20px" viewBox="0 -960 960 960" width="20px" fill="#e8eaed"><path d="M240-144v-72h480v72H240Zm240-144q-96 0-148.5-59.4T279-504.86V-816h97.21v317.09q0 52.85 26.43 85.88Q429.07-380 480.03-380q50.97 0 77.39-33.03 26.41-33.03 26.41-85.88V-816H681v311.14q0 98.06-52.5 157.46Q576-288 480-288Z"/></svg>';
    } else if (type === "strikethrough"){
        icon.innerHTML = '<svg height="20px" viewBox="0 -960 960 960" width="20px" fill="#e8eaed"><path d="M96-408v-72h768v72H96Zm336-144v-120H240v-96h480v96H528v120h-96Zm0 360v-144h96v144h-96Z"/></svg>';
    } else if (type === "comment"){
        icon.innerHTML = '<svg height="20px" viewBox="0 -960 960 960" width="20px" fill="#e8eaed"><path d="M240-384h480v-72H240v72Zm0-132h480v-72H240v72Zm0-132h480v-72H240v72ZM864-96 720-240H168q-29.7 0-50.85-21.15Q96-282.3 96-312v-480q0-29.7 21.15-50.85Q138.3-864 168-864h624q29.7 0 50.85 21.15Q864-821.7 864-792v696ZM168-312h582l42 42v-522H168v480Zm0 0v-480 480Z"/></svg>';
    }
    commentHeader.appendChild(icon);

    const commentFrom = document.createElement('div');
    commentFrom.classList.add('comment-from');
    commentFrom.textContent = employee_name;
    commentHeader.appendChild(commentFrom);

    const commentDate = document.createElement('div');
    commentDate.classList.add('comment-date');
    commentDate.textContent = 'Now';
    commentHeader.appendChild(commentDate);

    const deleteBtn = document.createElement('div');
    deleteBtn.classList.add('delete-btn');
    deleteBtn.onclick = function() {
        deleteRemark(test, dataCommentId);
    };
    deleteBtn.innerHTML = '<svg height="18px" viewBox="0 -960 960 960" width="18px" fill="#e8eaed"><path d="M312-144q-29.7 0-50.85-21.15Q240-186.3 240-216v-480h-48v-72h192v-48h192v48h192v72h-48v479.57Q720-186 698.85-165T648-144H312Zm336-552H312v480h336v-480ZM384-288h72v-336h-72v336Zm120 0h72v-336h-72v336ZM312-696v480-480Z"/></svg>';
    commentHeader.appendChild(deleteBtn);

    const commentContent = document.createElement('div');
    commentContent.classList.add('comment-content');
    if (type === "comment") {
        commentContent.textContent = content;
    } else {
        commentContent.classList.add('italics');
        if (type === "highlight") {
            commentContent.textContent = "Highlighted text";
        } else if (type === "underline") {
            commentContent.textContent = "Underlined text";
        }
        else if (type === "strikethrough") {
            commentContent.textContent = "Strikethrough text";
        }
    }
    commentBox.appendChild(commentContent);

    const addCommentBox2 = document.createElement('div');
    addCommentBox2.classList.add('add-comment-box-2');
    addCommentBox2.innerHTML = `<textarea class="comment-content-input" placeholder="Add comment">${content}</textarea><button class="send-button" onclick="updateCommentBox('${test}', '${dataCommentId}', '${type}')">Post</button>`;
    commentBox.appendChild(addCommentBox2);

    const remarksSection = document.getElementById('remarks-section');
    const addCommentBox = remarksSection.querySelector('.add-comment-box');

    remarksSection.insertBefore(commentBox, addCommentBox.nextSibling);
    addRemarkListeners();
    handleCommentClick([commentBox]);
    setTimeout(() => {commentBox.click();}, 1);
    addCommentBoxListeners();
}

function addCommentBox(test, id) {
    const remarksSection = document.getElementById('remarks-section');
    const textArea = remarksSection.querySelector('.add-comment');
    createCommentBox(test, id, 'comment', textArea.value);
    makeRemarkChanges(test, id, 'comment', textArea.value);
    textArea.value = '';
}

function updateCommentBox(test, id, type) {
    const remarksSection = document.getElementById('remarks-section');
    const commentBox = remarksSection.querySelector(`.comment-box[id="${id}"]`);
    const textArea = commentBox.querySelector('.comment-content-input');
    const textContent = commentBox.querySelector('.comment-content');
    textContent.innerHTML = textArea.value;
    const addCommentBox2 = commentBox.querySelector('.add-comment-box-2');
    addCommentBox2.style.display = 'none';
    textContent.style.display = 'block';
    textContent.classList.remove('italics');
    const commentDate = commentBox.querySelector('.comment-date');
    commentDate.innerHTML = 'Now';
    makeRemarkChanges(test, id, type, textArea.value);
}

function makeRemarkChanges(test, id, type, content) {
    const table_content = document.getElementsByTagName('table')[0].outerHTML;
    fetch('/make_remark_changes/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': id,
            'type': type,
            'content': content,
            'test_record_id': test,
            'table_content': table_content
        })
    });
}

function deleteRemark(test, id) {
    removeDiv(id);
    const table_content = document.getElementsByTagName('table')[0].outerHTML;
    const commentBox = document.getElementById(id);
    commentBox.remove();
    fetch('/delete_remark/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'id': id,
            'test_record_id': test,
            'table_content': table_content
        })
    });
}

function removeDiv(divId) {
    var divElement = document.querySelector(`[data-comment-id='${divId}']`);
    if (divElement) {
        var textNode = document.createTextNode(divElement.textContent);
        divElement.parentNode.replaceChild(textNode, divElement);
    }
}

function hideDeleteButton() {
    const commentBoxes = document.querySelectorAll('.comment-box');
    commentBoxes.forEach(commentBox => {
        const commentName = commentBox.querySelector('.comment-from').textContent.trim();
        const employeeName = employee_name;
        const commentDate = commentBox.querySelector('.comment-date').textContent.trim();
        const isRecent = commentDate === "Now" || commentDate.endsWith("min ago");
        if (commentName !== employeeName || !isRecent) {
            const deleteButton = commentBox.querySelector('.delete-btn');
            deleteButton.style.visibility = 'hidden';
        }
    });
}
hideDeleteButton();