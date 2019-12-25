<template>
  <div>
    <button type="button" class="btn btn-warning">Error Submit!</button>
    <form>
      <p>username: {{}}</p>
      <div class="form-group">
        <label for="TextareaError">Please input the error down</label>
        <textarea class="form-control" id="TextareaError" rows="4"></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
      <button type="button" class="btn btn-secondary">Cancel</button>
    </form>
  </div>
</template>

<script>
  import store from '../store.js'

  export default {
    data() {
      return {
        name: "ErrorBtn",
        username: '',
      }
    },

    created() {
      this.username = store.state.username;
    },

    methods: {

    }

  }


</script>

<style scoped>

</style>
