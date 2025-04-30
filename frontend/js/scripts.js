document.getElementById('orderForm').addEventListener('submit', (event) => {
    console.log('Form submission intercepted by scripts.js');
    event.preventDefault();

    const formData = {
        customerId: document.getElementById('customerId').value,
        item: document.getElementById('item').value,
        deliverySlot: document.getElementById('deliverySlot').value,
        instructions: document.getElementById('instructions').value
    };

    const hiddenForm = document.createElement('form');
    hiddenForm.method = 'POST';
    hiddenForm.action = event.target.action;
    hiddenForm.style.display = 'none';

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'data';
    input.value = JSON.stringify(formData);
    hiddenForm.appendChild(input);

    document.body.appendChild(hiddenForm);
    hiddenForm.submit();
});