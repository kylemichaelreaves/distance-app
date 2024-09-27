<template>
  <div>
    <h1>Find The Distance Between Two Addresses</h1>
    <div v-if="responseData.distance">
      <h4>The distance between <u>{{ origin.name }}</u> and <u>{{ destination.name }}</u> is</h4>
      <h2>{{ responseData.distance }} miles</h2>
    </div>

    <el-row class="centered-row">
      <el-col :span="10">
        <AutocompleteInput
            input-id="origin-input"
            placeholder="Enter origin address or landmark"
            @placeSelected="setOrigin"
            :country-restriction="{country: 'us'}"
        />
      </el-col>
      <el-col :span="10">
        <AutocompleteInput
            input-id="destination-input"
            placeholder="Enter destination address or landmark"
            @placeSelected="setDestination"
            :country-restriction="{country: 'us'}"
        />
      </el-col>
      <el-col :span="4">
        <el-button
            class="button"
            type="primary"
            @click="calculateDistance"
            :disabled="!origin && !destination">
          Calculate Distance
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>


<script setup lang="ts">
import AutocompleteInput from "./components/AutocompleteInput.vue";
import {ref, watch} from "vue";
import axios from "axios";

interface AutocompleteInputInterface {
  address?: string;
  lat?: number;
  lng?: number;
  name?: string;
  placeId?: string;
}

interface ResponseInterface {
  distance: number;
  cache: boolean;
}

const origin = ref<AutocompleteInputInterface>({
  address: '',
  lat: 0,
  lng: 0,
  name: '',
  placeId: '',
});

const destination = ref<AutocompleteInputInterface>({
  address: '',
  lat: 0,
  lng: 0,
  name: '',
  placeId: '',
});

const responseData = ref<ResponseInterface>({
  distance: 0,
  cache: false,
});

function setOrigin(place: AutocompleteInputInterface) {
  origin.value = place;
}

function setDestination(place: AutocompleteInputInterface) {
  destination.value = place;
}


async function calculateDistance() {
  if (!origin.value || !destination.value) {
    return;
  }
  try {
    const resp = await axios.post('http://127.0.0.1:8000/api/calculate-distance/', {
      origin: {
        address: origin.value.address,
        lat: origin.value.lat,
        lng: origin.value.lng,
      },
      destination: {
        address: destination.value.address,
        lat: destination.value.lat,
        lng: destination.value.lng,
      },
    })
    console.log('resp', resp);
    responseData.value = resp.data;
    console.log('responseData', responseData.value);
  } catch (error) {
    console.error(error);
  }
}

function resetDistance() {
  responseData.value = {
    distance: 0,
    cache: false,
  };
}

watch([origin, destination], () => {
  // if origin and destination are reset, reset the distance
  console.log('origin.value', origin.value);
  console.log('destination.value', destination.value);
  resetDistance();
});

</script>


<style scoped>
.centered-row {
  display: flex;
  align-items: baseline;
}

.button {
  margin-bottom: 10px;
}
</style>
