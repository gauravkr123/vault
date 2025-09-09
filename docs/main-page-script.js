const gross_to_monthly_calculator_updated_date = new Date('2025-09-09T14:44:19.443Z');
const monthly_to_gross_calculator_updated_date = new Date('2025-09-09T14:44:19.443Z');


window.addEventListener("load", function(){
    document.getElementById('monthly-to-gross-calculator-timestamp').textContent = "Updated at: " + monthly_to_gross_calculator_updated_date.toDateString();
    document.getElementById('gross-to-monthly-calculator-timestamp').textContent = "Updated at: " + gross_to_monthly_calculator_updated_date.toDateString();
});