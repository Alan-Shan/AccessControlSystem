<template>
  <div class="container h-100">
    <div class="row">
      <div class="col-md-12">
        <h1>Заявки</h1>
        <div v-if="loading" class="d-flex justify-content-center w-100 mt-5 mb-5">
          <div class="spinner-grow" role="status">
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
            <th scope="col">Статус</th>
            <th scope="col">Действия</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="request in requests" :key="request.id"
          >
            <td>{{ request.name + ' ' + request.surname + ' ' + request.patronymic }}</td>

            <td>{{ request.email }}</td>
            <td>{{ request.phone }}</td>
            <td>{{ request.purpose }}</td>
            <td>{{ request.document_type }}</td>
            <td>{{ request.document_number }}</td>
            <td>{{ request.creation_time }}</td>
            <td>{{ requestStatus(request.id)}}</td>
            <td>
              <div class="btn-group" role="group">

              <button type="button" class="btn btn-primary" v-on:click="accept(request.id)">
                      <font-awesome-icon icon="check"/>
                    </button>
                    <button type="button" class="btn btn-danger" v-on:click="reject(request.id)">
                      <font-awesome-icon icon="xmark"/>
                    </button>
                <button type="button" @click="redirectToRequest(request.id)" class="btn btn-secondary">
                  <font-awesome-icon icon="pen"/>
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
        <button @click="addRequest(null)" class="btn btn-primary">
          <font-awesome-icon icon="plus"/>
          Добавить заявку
        </button>
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
        redirectToRequest(id) {
          this.$router.push({ name: "SingleRequest", params: { id } });
        },
        addRequest() {
          this.$router.push("/singleRequest");
        },
        requestStatus(id) {
          switch (this.requests.find(request => request.id === id).status) {
            case "approved":
              return "Принята";
            case "rejected":
              return "Отклонена";
            default:
              return "В обработке";
          }
        },
        setGenericError() {
          this.message = {
            type: "error",
            text: "Произошла ошибка.",
          };
        },
        async reject(id) {
          try {
            await api.rejectRequest(id);
            // set requests with .request_id
            this.requests.find(r => {
              if (r.id === id) {
                r.status = "rejected";
                this.message = {
                  type: "success",
                  text: "Заявка отклонена.",
                };
              }
            })
          } catch (_) {
            this.setGenericError();
          }
        },
        async accept(id) {
          try {
            await api.approveRequest(id);
            this.requests.find(r => {
              if (r.id === id) {
                r.status = "approved";
                this.message = {
                  type: "success",
                  text: "Заявка принята.",
                };
              }
            })
          } catch (_) {
            this.setGenericError();
          }
        },
      }
}
</script>

<style scoped>

</style>