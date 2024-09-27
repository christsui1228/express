<template>
  <div class="shipping-form">
    <form @submit.prevent="submitForm">
      <div>
        <label for="srcAddress">Source Address:</label>
        <input id="srcAddress" v-model="srcAddress" required>
      </div>
      <div>
        <label for="destAddress">Destination Address:</label>
        <input id="destAddress" v-model="destAddress" required>
      </div>
      <div>
        <label for="weight">Weight (kg):</label>
        <input id="weight" v-model="weight" type="number" step="0.1" min="0.1" required>
      </div>
      <button type="submit">Calculate Shipping</button>
    </form>
    <div v-if="shippingOptions.length">
      <h2>Shipping Options:</h2>
      <div v-for="(option, index) in shippingOptions" :key="index">
        <p>Business Type: {{ option.businessTypeDesc }}</p>
        <p>Estimated Delivery Time: {{ option.deliverTime }}</p>
        <p>Fee: {{ option.fee }} {{ option.currency }}</p>
        <hr>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ShippingForm',
  data() {
    return {
      srcAddress: '',
      destAddress: '',
      weight: '',
      result: null
    }
  },
  computed: {
    shippingOptions() {
      if (this.result && this.result.apiResultData) {
        try {
          const apiResultData = JSON.parse(this.result.apiResultData)
          return apiResultData.msgData.deliverTmDto || []
        } catch (error) {
          console.error('Error parsing API result:', error)
          return []
        }
      }
      return []
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('http://localhost:8000/process_shipping', {
          src_address: this.srcAddress,
          dest_address: this.destAddress,
          weight: parseFloat(this.weight)
        })
        this.result = response.data
      } catch (error) {
        console.error('Error:', error)
        alert('An error occurred. Please try again.')
      }
    }
  }
}
</script>

<style scoped>
.shipping-form {
  max-width: 500px;
  margin: 0 auto;
}

form div {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
}

button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>