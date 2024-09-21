function populateModels(all_models) {
    const productTypeDropdown = document.getElementById("product");
    const modelNameDropdown = document.getElementById("model_name");
    const selectedProductType = productTypeDropdown.value;
    
    modelNameDropdown.innerHTML = "";
    const optionAllModels = document.createElement("option");
    optionAllModels.text = "All Models";
    optionAllModels.value = "";
    modelNameDropdown.appendChild(optionAllModels);
    
    all_models.forEach(model => {
        if (model.Product === selectedProductType) {
            const option = document.createElement("option");
            option.text = model.Model_Name_id;
            modelNameDropdown.appendChild(option);
            if (localStorage.getItem('selectedModel') === model.Model_Name_id) {
                option.selected = true;
            }
        } else if (selectedProductType === "") {
            const option = document.createElement("option");
            option.text = model.Model_Name_id;
            modelNameDropdown.appendChild(option);
            if (localStorage.getItem('selectedModel') === model.Model_Name_id) {
                option.selected = true;
            }
        }
    });
}
    
function populateTestName(testDetail) {
    const productTypeDropdown = document.getElementById("product");
    const testStageDropdown = document.getElementById("test_stage");
    const testNameDropdown = document.getElementById("test_name");
    const modelNameDropdown = document.getElementById("model_name");
    const selectedProductType = productTypeDropdown.value;
    const selectedTestStage = testStageDropdown.value;
    const selectedModelName = modelNameDropdown.value;

    testNameDropdown.innerHTML = "";
    const optionAllTests = document.createElement("option");
    optionAllTests.text = "All Tests";
    optionAllTests.value = "";
    testNameDropdown.appendChild(optionAllTests);

    let addedTests = [];

    testDetail.forEach(test => {
        if ((selectedProductType === "" || selectedProductType === test.ProductType) && (selectedTestStage === "" || selectedTestStage === test.TestStage) && (selectedModelName === "" || selectedModelName === test.ModelName)) {
            if (!addedTests.includes(test.TestName)) {
                const option = document.createElement("option");
                option.text = test.TestName;
                testNameDropdown.appendChild(option);
                addedTests.push(test.TestName);
            }
        }
    });
}