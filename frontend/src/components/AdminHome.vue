<template>
  <div class="container my-5">
    <div class="row p-4 pb-0 pe-lg-0 pt-lg-5 align-items-center rounded-3 border shadow-lg">
      <div class="col-lg-7 p-3 p-lg-5 pt-lg-3">
        <h1 class="display-4 fw-bold lh-1">TODO</h1>
        <p class="lead">Lorem ipsum, blah-blah-blah</p>
        <div class="d-grid gap-2 d-md-flex justify-content-md-start mb-4 mb-lg-3">
          <router-link to="ApplyForVisit">
            <button type="button" class="btn btn-primary btn-lg px-4 me-md-2 fw-bold">Заявки</button>
          </router-link>
          <router-link to="Main">
            <button type="button" class="btn btn-outline-secondary btn-lg px-4">Пользователи</button>
          </router-link>
        </div>
      </div>
      <div class="col-lg-4 offset-lg-1 p-0 overflow-hidden shadow-lg">
        <img class="rounded-lg-3" src="/building.jpg" alt="" width="700">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminHome"
}
</script>

<style scoped>

</style>