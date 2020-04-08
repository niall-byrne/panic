import React, { Component } from 'react';
import PropTypes from 'prop-types';
import DatePicker from 'react-datepicker';
import Select from 'react-select';
import { validateForm, validateField } from './itemFormValidator';
import 'react-datepicker/dist/react-datepicker.css';

class ItemForm extends Component {
  constructor(props) {
    super(props);
    this.formInit = {
      bestBefore: null,
      name: '',
      price: '',
      quantity: '',
      location: '',
      preferred: null,
      errors: '',
    };
    this.formPlaceholders = {
      defName: 'Item Name',
      defPrice: 'Est. Price',
      defQuantity: 'Quantity',
    };
    this.buttonText = 'Add New Item';
    this.state = { form: { ...this.formInit } };
    this.resetForm = this.resetForm.bind(this);
    this.changeField = this.changeField.bind(this);
    this.changeDate = this.changeDate.bind(this);
    this.submitForm = this.submitForm.bind(this);
  }

  changeField(event, field) {
    const { form } = this.state;
    const { state } = this.props;
    const { items } = state;
    const [errors, value] = validateField(event, field, items);
    form[field] = value;
    form.errors = errors;
    this.setState({ form });
  }

  changeDate(value) {
    // eslint-disable-next-line react/no-access-state-in-setstate,react/destructuring-assignment
    const form = { ...this.state.form };
    form.bestBefore = value;
    this.setState({ form });
  }

  resetForm() {
    const form = { ...this.formInit };
    this.setState({ form });
  }

  submitForm() {
    const { submit, state } = this.props;
    const { shelves, stores, items } = state;
    const { form } = this.state;
    const submittedForm = { ...form };
    let normalizedPreferred = [];

    const errors = validateForm(submittedForm, items);
    if (errors != null) {
      form.errors = errors;
      this.setState({ form });
      return;
    }

    // Put Form Data into API Friendly Objects
    const normalizedLocation = shelves.find((o) => o.name === form.location);
    if (form.preferred != null) {
      normalizedPreferred = form.preferred.map((d) => {
        const store = stores.find((o) => o.name === d.value);
        return { id: store.id, name: store.name };
      });
    }

    submittedForm.preferred = normalizedPreferred;
    submittedForm.location = normalizedLocation;
    delete submittedForm.errors;
    submit(submittedForm);
    this.resetForm();
  }

  render() {
    const { state } = this.props;
    const { shelves, stores } = state;
    const { form } = this.state;
    const {
      bestBefore,
      name,
      price,
      quantity,
      location,
      preferred,
      errors,
    } = form;
    const { defName, defPrice, defQuantity } = this.formPlaceholders;
    const shelfOptions = shelves.map((d) => {
      return { value: d.name, label: d.name };
    });
    const storeOptions = stores.map((d) => {
      return { value: d.name, label: d.name };
    });
    const shelfSelected = { value: location, label: location };
    return (
      <div className="component">
        <div>
          <form className="" onSubmit={this.submitForm}>
            <label htmlFor="bestBefore" className="section">
              Best Before Date:
              <DatePicker selected={bestBefore} onChange={this.changeDate} />
              <input name="bestBefore" type="text" hidden />
            </label>
            <br />
            <label htmlFor="name" className="section">
              Name:
              <input
                name="name"
                type="text"
                value={name}
                placeholder={defName}
                onChange={(e) => this.changeField(e, 'name')}
                required
              />
            </label>
            <br />
            <label htmlFor="price" className="section">
              Price:
              <input
                step="1"
                name="price"
                type="text"
                value={price}
                placeholder={defPrice}
                onChange={(e) => this.changeField(e, 'price')}
                required
              />
            </label>
            <br />
            <label htmlFor="quantity" className="section">
              Quantity:
              <input
                step="1"
                name="quantity"
                type="text"
                value={quantity}
                placeholder={defQuantity}
                onChange={(e) => this.changeField(e, 'quantity')}
                required
              />
            </label>
            <br />
            <label htmlFor="location" className="section">
              Location:
              <Select
                className="component"
                onChange={(e) => this.changeField(e.value, 'location')}
                options={shelfOptions}
                value={shelfSelected}
              />
              <input name="location" type="text" hidden />
            </label>
            <br />
            <label htmlFor="stores" className="section">
              <span>
                Preferred Stores:
                <Select
                  isMulti="true"
                  className="section"
                  name="stores"
                  value={preferred}
                  options={storeOptions}
                  onChange={(e) => this.changeField(e, 'preferred')}
                  multiple
                />
              </span>
              <input name="stores" type="text" hidden />
            </label>
            <br />
            <button type="button" onClick={this.submitForm}>
              {this.buttonText}
            </button>
            <button type="button" onClick={this.resetForm}>
              Clear Form
            </button>
          </form>
          {errors}
        </div>
      </div>
    );
  }
}

ItemForm.propTypes = {
  submit: PropTypes.func.isRequired,
  state: PropTypes.shape({
    items: PropTypes.arrayOf(PropTypes.object),
    shelves: PropTypes.arrayOf(PropTypes.object),
    stores: PropTypes.arrayOf(PropTypes.object),
  }).isRequired,
};

export default ItemForm;
