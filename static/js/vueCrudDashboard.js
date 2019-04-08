const AppComponent = {
    delimiters: ['[[', ']]'],  
    template: `<div class="container">

                    <div class="row">
                        <div class="col-6">
                            <div class="input-group mb-3">
                                <button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#addModal">Add Item</button>
                            </div>
                        </div>
                    </div>                    

                    <div class="row">
                        <div class="col-6">
                            <!-- Input Group -->
                            <div class="input-group mb-3">
                                <input type="text" v-model="matchString">
                                <div class="input-group-prepend">
                                    <button type="button" class="btn btn-primary btn-sm" @click="getItem">Search</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Table -->
                    <div class="table-responsive-md">
                        <table class="table table-dark">
                            <thead>
                                <tr>
                                    <th>
                                        Key
                                    </th>
                                    <th>
                                        Details
                                    </th>
                                    <th>
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
                                    <td>
                                        <!-- Button trigger modal -->
                                        <button type="button" class="btn btn-danger btn-sm" @click="selectItem(item)" data-toggle="modal" data-target="#deleteModal">Delete</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                        <!-- Add Modal -->
                        <div class="modal fade" id="addModal" tabindex="-1" role="dialog" aria-labelledby="addModalLabel" aria-hidden="true">
                            <div class="modal-dialog" role="document">
                                <div class="modal-content">
                                    <div class="modal-body">
                                        <form>
                                        <div class="form-group">
                                            <label class="col-form-label">Key:</label>
                                            <input type="text" class="form-control" v-model="addItem.key">
                                        </div>
                                        <div class="form-group">
                                            <label class="col-form-label">Details:</label>
                                            <input type="text" class="form-control" v-model="addItem.details">
                                        </div>
                                        </form>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                        <button type="button" class="btn btn-primary" data-dismiss="modal" @click="setItem">Add Item</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Delete Modal -->
                        <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalCenterTitle" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered" role="document">
                                <div class="modal-content">
                                    <div class="modal-body">
                                        Are you sure you want to delete Key: [[ selectedItem.key ]]
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary btn-sm" data-dismiss="modal">Close</button>
                                        <button type="button" class="btn btn-danger btn-sm" data-dismiss="modal" @click="deleteItem(selectedItem)">Delete</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                     </div>
               </div>`,
    data() {
        return {
            tableItems: [],
            apiURL: "http://0.0.0.0:5000/dashboard_api",
            selectedItem: {},
            addItem: {},
            matchString: ""
        }
    },
    created() {
        this.getItems()
    },
    methods: {
        getItems: function() {
            axios.get(`http://0.0.0.0:5000/dashboard_api`)
            .then(response => {
                this.tableItems = response.data
            })
            .catch(e => {
                this.errors.push(e)
            })
        },
        getItem: function() {
            axios.get(`http://0.0.0.0:5000/dashboard_api?key=` + this.matchString)
            .then(response => {
                this.tableItems = response.data
                this.matchString = ""
            })
            .catch(e => {
                this.errors.push(e)
            })
        },
        deleteItem: function(deletedItem) {
            axios({
                method: 'delete',
                url: this.apiURL,
                data: deletedItem,
                headers: {
                'Content-Type': 'application/json'
                }
            }).then(() => {
                this.getItems()
            })
            .catch(e => {
                this.errors.push(e)
            })
        },
        setItem: function() {
            axios({
                method: 'post',
                url: this.apiURL,
                data: this.addItem,
                headers: {
                'Content-Type': 'application/json'
                }
            }).then(() => {
                this.getItems()
                this.clearAddItem()
            })
            .catch(e => {
                this.errors.push(e)
            })
        },
        selectItem: function(itemSelected){
            this.selectedItem = itemSelected
        },
        clearAddItem: function() {
            this.addItem = {}
        }
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