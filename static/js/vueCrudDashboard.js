const AppComponent = {
    delimiters: ['[[', ']]'],  
    template: `<div>
                 <table class="table table-dark">
                    <thead>
                      <tr>
                        <th>
                          Key
                        </th>
                        <th>
                          Details
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in tableItems">
                        <td>
                          [[ item.key ]]
                        </td>
                        <td>
                          [[ item.details ]]
                        </td>
                      </tr>
                    </tbody>
                 </table>
               </div>`,
    data() {
        return {
            tableItems: []
        }
    },
    created() {
        // TODO: Turn this to a method
        axios.get(`http://0.0.0.0:5000/dashboard_api?key=0`)
        .then(response => {
            this.tableItems = response.data
        })
        .catch(e => {
            this.errors.push(e)
        })
    }
};

new Vue({  
    el: '#app',
    template:`
    <div id="vue-application">
        <app-component></app-component>
    </div>
    `
       ,
    components: {  
        AppComponent,  
    },  
});