function modifyCardContainer(card, pick, club) {
    const cardContainer = card.parentElement;
    const sumContainer = cardContainer.parentElement;
    const productName = card.querySelector('.card-product').textContent.trim();
    const modelName = card.querySelector('.card-model').textContent.trim();

    let newContainer = document.createElement('div');
    newContainer.classList.add('scrollcontainer');
    if(pick || !club){
        let cards = Array.from(cardContainer.children)
        for(let i = 0; i < cards.length; i++){
            childProduct = cards[i].querySelector('.card-product').textContent.trim();
            childModel = cards[i].querySelector('.card-model').textContent.trim();
            if(productName === childProduct && modelName === childModel){
                newContainer.appendChild(cards[i]);
                break;
            }
            newContainer.appendChild(cards[i]);
        }
        sumContainer.insertBefore(newContainer, cardContainer);
    } else {
        let cards = Array.from(cardContainer.children)
        if(cardContainer.nextElementSibling.nextElementSibling){
            for(let i = cards.length-1; i > -1; i--){
                cardContainer.nextElementSibling.nextElementSibling.insertBefore(cards[i], cardContainer.nextElementSibling.nextElementSibling.firstChild);
            }
        }
    }
    return newContainer;
}

function placeCloneTable(card, cloneTable, pick, club, last_card) {
    const cardParent = card.parentElement;
    const sumParent = cardParent.parentElement;
    newContainer = modifyCardContainer(card, pick, club);
    if(pick || !club){
        if(last_card){
            sumParent.insertBefore(cloneTable, cardParent);
            cardParent.remove();
        } else {
            sumParent.insertBefore(cloneTable, cardParent);
        }
    } else {
        sumParent.removeChild(cardParent.nextElementSibling);
        if(!last_card){
            cardParent.remove();
        }
    }
}
        
function getCloneTable(card, pick, club) {
    const productName = card.querySelector('span.card-product').textContent.trim();
    const modelName = card.querySelector('span.card-model').textContent.trim();

    const mainTable = document.querySelectorAll('.main-table');
    const mainTableRows = Array.from(mainTable[mainTable.length - 1].querySelector('tbody').children);
    const cloneTable = mainTable[mainTable.length - 1].cloneNode(true);
    const cloneTableBody = cloneTable.querySelector('tbody');
    let remRows = mainTableRows.length;
    mainTableRows.forEach(row => {
        if(row.children[0].colSpan !== 5){
            if(row.children[1].textContent.trim() == productName && row.children[2].textContent.trim() == modelName){
                if(pick || !club){
                    row.querySelector('td button').click();
                    cloneTableBody.innerHTML = row.outerHTML + row.nextElementSibling.outerHTML;
                    row.nextElementSibling.style.display = "none";
                    row.style.display = "none";
                } else {
                    row.querySelector('td button').click();
                    row.nextElementSibling.removeAttribute('style');
                    row.removeAttribute('style');
                }
            }
            if(row.getAttribute('style')){
                remRows--;
                remRows--;
            }
        }
    });
    if(remRows == 0) {
        mainTable[mainTable.length - 1].style.display = "none";
    } else if (mainTable[mainTable.length - 1].getAttribute('style')) {
        mainTable[mainTable.length - 1].removeAttribute('style');
    }
    cloneTable.querySelector('thead').querySelector('tr').querySelector('th').children[0].remove();

    const newTableContainer = document.createElement('div');
    newTableContainer.classList.add('table-containers');
    newTableContainer.classList.add('card-table-containers');
    newTableContainer.appendChild(cloneTable);

    return newTableContainer;
}

function fetchModelRow(card) {
    let pick, club, last_card;
    if(card.nextElementSibling){pick = true;}
    else {pick = false;}
    if(card.parentElement.nextElementSibling){club = true;}
    else {club = false;}
    if(card.nextElementSibling){last_card = false;}
    else {
        if(card.parentElement.nextElementSibling && card.parentElement.nextElementSibling.nextElementSibling){
            last_card = false;
        }
        else {last_card = true;}
    }
    const cloneTable = getCloneTable(card, pick, club);
    placeCloneTable(card, cloneTable, pick, club, last_card);
}