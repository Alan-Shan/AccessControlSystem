<template>
  <div class="container h-100">
    <div class="row">
      <div class="col-md-12">
        <h1>Заявки</h1>
        <div v-if="loading" class="d-flex justify-content-center w-100 mt-5">
          <div class="spinner-grow" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div v-if="message.text" class="alert" :class="alertClass" role="alert">
          {{ message.text }}
        </div>
        <table v-if="!loading && requests.length" class="table table-responsive table-bordered">
          <thead>
          <tr>
            <th scope="col">ФИО</th>
            <th scope="col">Email</th>
            <th scope="col">Телефон</th>
            <th scope="col">Цель визита</th>
            <th scope="col">Тип документа</th>
            <th scope="col">Номер документа</th>
            <th scope="col">Дата создания</th>
            <th scope="col">Дата обновления</th>
            <th scope="col">Статус</th>
            <th scope="col">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="request in requests" :key="request.id">
            <td>{{ request.name + ' ' + request.surname + ' ' +  request.patronymic }}</td>

            <td>{{ request.email }}</td>
            <td>{{ request.phone }}</td>
            <td>{{ request.visitPurpose }}</td>
            <td>{{ request.document_type }}</td>
            <td>{{ request.document_number }}</td>
            <td>{{ request.status }}</td>
            <td>
              <button type="button" class="btn btn-primary" v-on:click="accept(request.id)">a</button>
              <button type="button" class="btn btn-danger" v-on:click="reject(request.id)">D</button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "RequestsList",
  data() {
    return {
      requests: [],
      alertClasses: {
        success: "alert-success",
        error: "alert-danger",
        info: "alert-info",
      },
      message: {
        type: "",
        text: "",
      },
      loading: true,
    }
  },
  computed: {
    alertClass() {
      return this.alertClasses[this.message.type];
    }
  },
  async mounted() {
    try {
      const response = await api.getRequests();
      this.requests = response.data;
      if (!this.requests.length) {
        this.message = {
          type: "info",
          text: "В данный момент заявки в системе отсутствуют",
        };
      }
    } catch (e) {
      this.message = {
        type: "error",
        text: "Произошла ошибка при загрузке заявок",
      };
      console.log(e);
    } finally {
      console.log("finally");
      this.loading = false;
    }
  },
  methods:
      {
        async reject(id) {
          try {
            await api.rejectRequest(id);
          } catch (e) {
            console.log(e);
          }
        },
        async accept(id) {
          try {
            await api.approveRequest(id);
          } catch (e) {
            console.log(e);
          }
        },
      }
}
</script>

<style scoped>

</style>