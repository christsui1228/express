<template>
  <div id="app">
    <h1>Shipping Calculator</h1>
    <ShippingForm />
  </div>
</template>

<script>
import ShippingForm from './components/ShippingForm.vue'

export default {
  name: 'App',
  components: {
    ShippingForm
  }
}
</script>