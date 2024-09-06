// JavaScript function to populate the model list based on the selected product type
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
        } else if (selectedProductType === "") {
            const option = document.createElement("option");
            option.text = model.Model_Name_id;
            modelNameDropdown.appendChild(option);
        }
    });
}
    
function populateTestName(testDetail) {
    // const testDetail = {{ test|safe;
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

    testDetail.forEach(test => {
        if ((selectedProductType === "" || selectedProductType === test.ProductType) && (selectedTestStage === "" || selectedTestStage === test.TestStage) && (selectedModelName === "" || selectedModelName === test.Model_Name_id)) {
            const option = document.createElement("option");
            option.text = test.TestName;
            testNameDropdown.appendChild(option);
        }
        // const s = item.TestStage;

        // if (selectedProductType === "" && selectedTestStage === "") {
        //     // If both product type and test stage are not selected, show all test names
        //     const option = document.createElement("option");
        //     option.text = item.TestName;
        //     testNameDropdown.appendChild(option);
        // } else if (selectedProductType === "") {
        //     // If only test stage is selected, filter by test stage
        //     if ((s[0] === '1' && selectedTestStage === "DVT") ||
        //         (s[1] === '1' && selectedTestStage === "PP") ||
        //         (s[2] === '1' && selectedTestStage === "MP")) {
        //         const option = document.createElement("option");
        //         option.text = item.TestName;
        //         testNameDropdown.appendChild(option);
        //     }
        // } else if (selectedTestStage === "") {
        //     // If only product type is selected, filter by product type
        //     if (item.ProductType === selectedProductType) {
        //         const option = document.createElement("option");
        //         option.text = item.TestName;
        //         testNameDropdown.appendChild(option);
        //     }
        // } else {
        //     // If both product type and test stage are selected, filter by both
        //     if (item.ProductType === selectedProductType && (
        //         (s[0] === '1' && selectedTestStage === "DVT") ||
        //         (s[1] === '1' && selectedTestStage === "PP") ||
        //         (s[2] === '1' && selectedTestStage === "MP"))) {
        //         const option = document.createElement("option");
        //         option.text = item.TestName;
        //         testNameDropdown.appendChild(option);
        //     }
        // }
    });
}