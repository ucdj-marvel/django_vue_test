<template>
  <div class="home">
    <div class="row no-gutters">

    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
};
</script>
<style lang="scss" scoped>
  .home {
    padding-top: 1rem;
    align-items: center;
  }
  .no-gutters {
    margin:1rem;
    padding:0;
    .col,
    [class*="col-"] {
      margin: 0;
      padding:0.5rem 1rem;
    }
  }

</style>
