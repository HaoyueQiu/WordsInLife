<template>
  <div class="alert" role="alert" v-bind:class="'alert-' + variant">
    {{ message }}
  </div>
</template>

<script>
export default {
  //props获取从父组件传递过来的消息，因此在template中才能够使用 message和variant
  props: ['variant', 'message']
}
</script>
