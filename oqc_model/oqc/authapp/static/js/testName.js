function populateTimeline(timeline_dvt, timeline_pp, timeline_mp) {
    const dvt = [``, ``];
    const pp = [``, ``];
    const mp = [``, ``];
    if (timeline_dvt[0]) {
        dvt[0] = `value=${timeline_dvt[0]}`;
    }
    if (timeline_dvt[1]) {
        dvt[1] = `value=${timeline_dvt[1]}`;
    }
    if (timeline_pp[0]) {
        pp[0] = `value=${timeline_pp[0]}`;
    }
    if (timeline_pp[1]) {
        pp[1] = `value=${timeline_pp[1]}`;
    }
    if (timeline_mp[0]) {
        mp[0] = `value=${timeline_mp[0]}`;
    }
    if (timeline_mp[1]) {
        mp[1] = `value=${timeline_mp[1]}`;
    }
    const mobileHTML = `<div class="mobile-tg">
                            <div class="form-group timeline-group">
                                <label>DVT Timeline <span style="font-size: 12px; font-weight: 300;">(Leave empty if not decided yet)</span></label>
                                <div class="timeline">
                                    Start Date: <input ${dvt[0]} type="date" class="timeline-input form-control" id="dvt" name="dvt-start-date" placeholder="Enter NA if not decided yet">
                                </div>
                                <div class="timeline">
                                    End Date: <input ${dvt[1]} type="date" class="timeline-input form-control" id="dvt" name="dvt-end-date" placeholder="Enter NA if not decided yet">
                                </div>
                            </div>
                            <div class="form-group timeline-group">
                                <label>PP Timeline <span style="font-size: 12px; font-weight: 300;">(Leave empty if not decided yet)</span></label>
                                <div class="timeline">
                                    Start Date: <input ${pp[0]} type="date" class="timeline-input form-control" id="pp" name="pp-start-date" placeholder="Enter NA if not decided yet">
                                </div>
                                <div class="timeline">
                                    End Date: <input ${pp[1]} type="date" class="timeline-input form-control" id="pp" name="pp-end-date" placeholder="Enter NA if not decided yet">
                                </div>
                            </div>
                            <div class="form-group timeline-group">
                                <label>MP Timeline <span style="font-size: 12px; font-weight: 300;">(Leave empty if not decided yet)</span></label>
                                <div class="timeline">
                                    Start Date: <input ${mp[0]} type="date" class="timeline-input form-control" id="mp" name="mp-start-date" placeholder="Enter NA if not decided yet">
                                </div>
                                <div class="timeline">
                                    End Date: <input ${mp[1]} type="date" class="timeline-input form-control" id="mp" name="mp-end-date" placeholder="Enter NA if not decided yet">
                                </div>
                            </div>
                        </div>`;
    const desktopHTML = `<div class="desktop-tg">
                            <div class="form-group timeline-group">
                                <label>Timeline <span style="font-size: 12px; font-weight: 300;">(Leave empty if not decided yet)</span></label>
                                <table class="desktop-tg-table">
                                    <colgroup>
                                        <col>
                                        <col>
                                        <col>
                                    </colgroup>
                                    <thead>
                                        <tr>
                                            <th></th>
                                            <th>Start Date</th>
                                            <th>End Date</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <th>DVT</th>
                                            <td>
                                                <div>
                                                    <input ${dvt[0]} type="date" class="timeline-input form-control" id="dvt" name="dvt-start-date" placeholder="Enter NA if not decided yet">
                                                </div>
                                            </td>
                                            <td>
                                                <div>
                                                    <input ${dvt[1]} type="date" class="timeline-input form-control" id="dvt" name="dvt-end-date" placeholder="Enter NA if not decided yet">
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th>PP</th>
                                            <td>
                                                <div>
                                                    <input ${pp[0]} type="date" class="timeline-input form-control" id="pp" name="pp-start-date" placeholder="Enter NA if not decided yet">
                                                </div>
                                            </td>
                                            <td>
                                                <div>
                                                    <input ${pp[1]} type="date" class="timeline-input form-control" id="pp" name="pp-end-date" placeholder="Enter NA if not decided yet">
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th>MP</th>
                                            <td>
                                                <div>
                                                    <input ${mp[0]} type="date" class="timeline-input form-control" id="mp" name="mp-start-date" placeholder="Enter NA if not decided yet">
                                                </div>
                                            </td>
                                            <td>
                                                <div>
                                                    <input ${mp[1]} type="date" class="timeline-input form-control" id="mp" name="mp-end-date" placeholder="Enter NA if not decided yet">
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>`;
    const timelineDevice = document.querySelector('.timeline-device');

    if (window.innerWidth > 600) {
        timelineDevice.innerHTML = desktopHTML;
    } else {
        timelineDevice.innerHTML = mobileHTML;
    }
}

function populateTests(DVT, PP, MP, dvt, pp, mp) {
    for(let i=0; i<dvt.length; i++) {
        if(dvt[i] === 1) {
            dvt[i] = true;
        } else {
            dvt[i] = false;
        }
    }

    for(let i=0; i<pp.length; i++) {
        if(pp[i] === 1) {
            pp[i] = true;
        } else {
            pp[i] = false;
        }
    }

    for(let i=0; i<mp.length; i++) {
        if(mp[i] === 1) {
            mp[i] = true;
        } else {
            mp[i] = false;
        }
    }

    let addedTests = [];
    const templateRow = document.getElementById('templateRow');
    const tableBody = templateRow.parentElement;
    for (let i = 0; i < DVT.length; i++) {
        const multiSelect = document.querySelector(`select.multiple-selections#dvt-options`);
        const option = multiSelect.querySelector(`option[value="${DVT[i]}"]`);
        if (!addedTests.includes(DVT[i])) {
            addedTests.push(DVT[i]);
            const tempRow = templateRow.cloneNode(true);
            tempRow.removeAttribute('id');
            tempRow.setAttribute('testName', DVT[i]);
            tempRow.querySelector('th').textContent = DVT[i];
            tempRow.querySelector('td input#dvt').checked = dvt[i];
            option.selected = true;
            tempRow.querySelector('td input#dvt').disabled = false;
            tempRow.querySelector('td input#pp').disabled = !(PP.includes(DVT[i]));
            tempRow.querySelector('td input#mp').disabled = !(MP.includes(DVT[i]));
            tableBody.appendChild(tempRow);
        } else {
            const testRow = tableBody.querySelector(`[testName="${DVT[i]}"]`);
            testRow.querySelector('td input#dvt').checked = dvt[i];
            option.selected = true;
        }
    }

    for (let i = 0; i < PP.length; i++) {
        const multiSelect = document.querySelector(`select.multiple-selections#pp-options`);
        const option = multiSelect.querySelector(`option[value="${PP[i]}"]`);
        if (!addedTests.includes(PP[i])) {
            addedTests.push(PP[i]);
            const tempRow = templateRow.cloneNode(true);
            tempRow.removeAttribute('id');
            tempRow.setAttribute('testName', PP[i]);
            tempRow.querySelector('th').textContent = PP[i];
            tempRow.querySelector('td input#pp').checked = pp[i];
            option.selected = true;
            tempRow.querySelector('td input#dvt').disabled = true;
            tempRow.querySelector('td input#mp').disabled = !(MP.includes(PP[i]));
            tableBody.appendChild(tempRow);
        } else {
            const testRow = tableBody.querySelector(`[testName="${PP[i]}"]`);
            testRow.querySelector('td input#pp').checked = pp[i];
            option.selected = true;
        }
    }

    for (let i = 0; i < MP.length; i++) {
        const multiSelect = document.querySelector(`select.multiple-selections#mp-options`);
        const option = multiSelect.querySelector(`option[value="${MP[i]}"]`);
        if (!addedTests.includes(MP[i])) {
            addedTests.push(MP[i]);
            const tempRow = templateRow.cloneNode(true);
            tempRow.removeAttribute('id');
            tempRow.setAttribute('testName', MP[i]);
            tempRow.querySelector('th').textContent = MP[i];
            tempRow.querySelector('td input#mp').checked = mp[i];
            option.selected = true;
            tempRow.querySelector('td input#dvt').disabled = true;
            tempRow.querySelector('td input#pp').disabled = true;
            tableBody.appendChild(tempRow);
        } else {
            const testRow = tableBody.querySelector(`[testName="${MP[i]}"]`);
            testRow.querySelector('td input#mp').checked = mp[i];
            option.selected = true;
        }
    }
    templateRow.remove();
}

function fillMultiSelect(selectedBox) {
    const testName = selectedBox.parentElement.parentElement.getAttribute('testName');
    const stage = selectedBox.id;
    const selected = selectedBox.checked;
    const multiSelect = document.querySelector(`select.multiple-selections#${stage}-options`);
    const option = multiSelect.querySelector(`option[value="${testName}"]`);
    if (selected) {option.selected = true;} 
    else {option.selected = false;}
}

// function singleSelect(selectedBox) {
//     const checkboxes = document.querySelectorAll('.single-select-checkboxes');
//     checkboxes.forEach(checkbox => {
//         if (checkbox !== selectedBox) {
//             checkbox.checked = false;
//         }
//     });

//     const stage_id = selectedBox.getAttribute('id');
//     const multiSelect = document.querySelectorAll('.multi-select');
//     const timelines = document.querySelectorAll('.timeline-group');

//     if (selectedBox.checked) {
//         if (stage_id === 'stage-dvt') {
//             multiSelect.forEach(multiSel => {
//                 if (multiSel.id !=='dvt-options') {
//                     multiSel.parentElement.parentElement.style.display = 'none';
//                 } else {
//                     multiSel.parentElement.parentElement.style.display = 'block';
//                 }
//             });
//             timelines.forEach(timeline => {
//                 if (timeline.querySelector('input').id !=='dvt') {
//                     timeline.style.display = 'none';
//                 } else {
//                     timeline.style.display = 'flex';
//                 }
//             });
//         }
//         else if (stage_id === 'stage-pp') {
//             multiSelect.forEach(multiSel => {
//                 if (multiSel.id !=='pp-options') {
//                     multiSel.parentElement.parentElement.style.display = 'none';
//                 } else {
//                     multiSel.parentElement.parentElement.style.display = 'block';
//                 }
//             });
//             timelines.forEach(timeline => {
//                 if (timeline.querySelector('input').id !=='pp') {
//                     timeline.style.display = 'none';
//                 } else {
//                     timeline.style.display = 'flex';
//                 }
//             });
//         }
//         else if (stage_id === 'stage-mp') {
//             multiSelect.forEach(multiSel => {
//                 if (multiSel.id !=='mp-options') {
//                     multiSel.parentElement.parentElement.style.display = 'none';
//                 } else {
//                     multiSel.parentElement.parentElement.style.display = 'block';
//                 }
//             });
//             timelines.forEach(timeline => {
//                 if (timeline.querySelector('input').id !=='mp') {
//                     timeline.style.display = 'none';
//                 } else {
//                     timeline.style.display = 'flex';
//                 }
//             });
//         }
//     }
//     else {
//         multiSelect.forEach(multiSel => {
//             multiSel.parentElement.parentElement.style.display = 'none';
//         });
//         timelines.forEach(timeline => {
//             timeline.style.display = 'none';
//         });
//     }
// }

// document.querySelectorAll('.multi-select').forEach(ms => ms.parentElement.parentElement.style.display = 'none');
// document.querySelectorAll('.timeline-group').forEach(tg => tg.style.display = 'none');