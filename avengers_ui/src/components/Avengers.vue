<template lang="pug">
.row
  .col-md
    .row
      .col-md-4.mt-3.mb-2
        .input-group
          .input-group-prepend.px-3.py-2.border.bg-light
            i( class='fa fa-filter' )
          input.w-75( v-model="filterString" )

      .col-md-2
        label Deaths
        v-select( :options="deathCounts" v-model="deathsFilter" )

      .col-md-2
        label Returns
        v-select( :options="returnCounts" v-model="returnsFilter" )

      .col.md-1
        label.d-block Average Deaths
        h4 {{ sortedFilteredAvengers.length ? averageDeaths : 0 }}

      .col.md-1( v-if="probability" )
        h4.d-block {{ selectedAvenger.name }}
        h5 {{ probability }}% Chance of Return

    .row
      table.table.table-responsive.table-striped.table-bordered( v-if="avengers" )
        thead
          tr
            th( scope="col" @click="sortBy('name')" )
              | Name
              i.fas.fa-sort
            th( scope="col" @click="sortBy('deaths')" )
              | Deaths
              i.fas.fa-sort
            th( scope="col" @click="sortBy('returns')" )
              | Returns
              i.fas.fa-sort
            th( scope="col" @click="sortBy('url')" )
              | URL
              i.fas.fa-sort
            th( scope="col" @click="sortBy('appearances')" )
              | Appearances
              i.fas.fa-sort
            th( scope="col" @click="sortBy('current')" )
              | Is Active
              i.fas.fa-sort
            th( scope="col" @click="sortBy('gender')" )
              | Gender
              i.fas.fa-sort
            th( scope="col" @click="sortBy('probationary')" )
              | Probationary Date
              i.fas.fa-sort
            th( scope="col" @click="sortBy('full_reserve')" )
              | Join Date
              i.fas.fa-sort
            th( scope="col" @click="sortBy('year')" )
              | Year Joined
              i.fas.fa-sort
            th( scope="col" @click="sortBy('years_since_joining')" )
              | Years since joining
              i.fas.fa-sort
            th( scope="col" @click="sortBy('honorary')" )
              | Membership
              i.fas.fa-sort
            th( scope="col" @click="sortBy('notes')" )
              | Notes
              i.fas.fa-sort
            th( scope="col" ) Actions
        tbody
          tr( v-for="avenger in sortedFilteredAvengers" :key="avenger.id" )
            td {{ avenger.name }}
            td {{ avenger.deaths.length }}
            td {{ avenger.deaths[avenger.deaths.length - 1].returned ? avenger.deaths.length : avenger.deaths.length - 1 }}
            td {{ avenger.url }}
            td {{ avenger.appearances }}
            td {{ avenger.current ? 'Yes' : 'No' }}
            td {{ avenger.gender }}
            td {{ avenger.probationary }}
            td {{ avenger.full_reserve }}
            td {{ avenger.year }}
            td {{ avenger.years_since_joining }}
            td {{ avenger.honorary }}
            td {{ avenger.notes }}
            td( @click="getReturnProbability( avenger )" )
              i.fas.fa-vial

</template>

<script>
import _ from 'lodash';

export default {
  name: "Avengers",

  data() {
    return {
      avengers: [],
      deathsFilter: null,
      returnsFilter: null,
      filterString: "",
      reverseSort: false,
      sortColumn: "id",
      probability: null,
      selectedAvenger: null
    }
  },

  computed: {
    averageDeaths() {
      const deaths = _.sumBy( this.sortedFilteredAvengers, ( avenger ) => {
        return avenger.deaths.length
      } )

      return _.toNumber( deaths / this.sortedFilteredAvengers.length ).toFixed( 2 )
    },

    deathCounts() {
      if ( this.avengers ) {
        const deaths = new Set()

        _.forEach( this.avengers, (avenger) => {
          deaths.add(avenger.deaths.length)
        })

        return [ ...deaths ].sort()
      }
      else {
        return []
      }
    },

    returnCounts() {
      if ( this.avengers ) {
        const returns = new Set()

        _.forEach( this.avengers, ( avenger ) => {
          const returnCount = avenger.deaths[avenger.deaths.length - 1].returned ? avenger.deaths.length : avenger.deaths.length - 1

          if ( !this.deathsFilter || returnCount <= this.deathsFilter ) {
            returns.add( returnCount )
          }
        } )

        return [ ...returns ].sort()
      }
      else {
        return []
      }
    },

    sortedAvengers() {
      const avengers = _.sortBy( this.avengers, ( avenger ) => {
        if ( Object.keys(avenger).includes( this.sortColumn ) ) {
          return avenger[ this.sortColumn ]
        }
        else if ( this.sortColumn == 'returns' ) {
          return avenger.deaths[avenger.deaths.length - 1].returned ? avenger.deaths.length : avenger.deaths.length - 1
        }
        else if ( this.sortColumn == 'deaths' ) {
          return avenger.deaths.length
        }
        else {
          return avenger.id
        }
      })

      if ( this.reverseSort ) {
        return _.reverse( avengers )
      }
      else {
        return avengers
      }
    },

    sortedFilteredAvengers() {
      const avengers = _.filter( this.sortedAvengers, (avenger) => {
        return _.some(Object.values(avenger), (value) => {
          return _.includes(_.toString(value).toLowerCase(), this.filterString.toLowerCase())
        })
      })

      return _.filter( avengers, ( avenger ) => {
        const returnsCount = avenger.deaths[avenger.deaths.length - 1].returned ? avenger.deaths.length : avenger.deaths.length - 1

        let deaths = this.deathsFilter === null
        let returns = this.returnsFilter === null

        if ( !deaths ) {
            deaths = avenger.deaths.length === this.deathsFilter
        }
        if ( !returns ) {
          returns = returnsCount === this.returnsFilter
        }

        return deaths && returns
      })
    }
  },

  mounted() {
    this.debounceGet()
  },

  methods: {
    debounceGet() {
      const get = _.debounce( this.get, 500)
      get()
    },

    get() {
      this.$axios
          .get( 'avengers', { params: { filter: this.filterString } } )
          .then( response => {
            this.avengers = response.data;
          })
    },

    sortBy( columnName ) {
      if ( this.sortColumn === columnName ) {
        this.reverseSort = !this.reverseSort
      }

      this.sortColumn = columnName
    },

    getReturnProbability( avenger ) {
      this.axios
          .get( `avengers/${ avenger.id }/probability`)
          .then( ( response ) => {
            this.probability = _.toInteger(response.data * 100)
            this.selectedAvenger = avenger
          })
    }
  }
};
</script>
