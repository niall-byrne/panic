// Validators for the itemForm

export function validateField(event, field, items) {
  // Returns validation errors (if any) and the cleaned contents of the form field
  let testValue;
  let errors = '';
  let value;
  switch (field) {
    case 'name':
      value = event.target.value;
      testValue = items.find((o) => o.name === value);
      if (testValue) errors = 'Item with this name already exists.';
      break;
    case 'quantity':
      value = event.target.value;
      testValue = value.replace(/\D/, '');
      errors = testValue === value ? errors : 'Quantity can by numeric only.';
      value = testValue;
      break;
    case 'price':
      value = event.target.value;
      testValue = value.replace(/[^0-9|^.]+/g, '');
      errors = testValue === value ? errors : 'Price can by numeric only.';
      value = testValue;
      break;
    case 'location':
      value = event;
      break;
    case 'preferred':
      value = event;
      break;
    default:
      value = event.target.value;
      break;
  }
  return [errors, value];
}

export function validateForm(data, items) {
  // Returns null if there are no errors, or a string containing form errors
  if (items.find((o) => o.name === data.name))
    return 'Item with this name already exists.';
  if (data.name.length < 1) return 'Name cannot be blank.';
  if (data.price.length < 1) return 'Price cannot be blank.';
  if (data.quantity.length < 1) return 'Quantity cannot be blank.';
  if (data.location === '') return 'Item must have a shelf location.';
  return null;
}

export default validateField;
