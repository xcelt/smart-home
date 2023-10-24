import './App.css';
import axios from "axios"
import React, { Component } from 'react'
import CustomModal from './components/Modal'

class App extends Component {
  constructor(props) {
    super(props);
    this.state={
      CustomModal: true,
      viewCompleted: true,
          activeItem: {
        title: "",
        description: "",
        completed: false,
      },
      todoList: []
    };
  }

  componentDidMount() {
    this.refreshList();
  }

  refreshList = () => {
    axios
    .get("http://localhost:8000/api/tasks/")
    .then(res => this.setState({ todoList : res.data }))
    .catch(err => console.log(err))
  };

  // Create a toggle property
  toggle= () => {
    this.setState({ modal: !this.state.modal });
  };

  handleSubmit = item => {
    this.toggle();
    if (item.id) {
      axios.put(`http://localhost:8000/api/tasks/${item.id}/` , item)
      axios.then(res => this.refreshList())
    }
    axios.post("http://localhost:8000/api/tasks", item)
    axios.then(res => this.refreshList()) // He calls this one a "promise"
  };

  handleDelete = item => {
    if (item.id) {
      axios
       .delete(`http://localhost:8000/api/tasks/${item.id}/`)
       .then(res => this.refreshList())
    }
  };

  createItem = () => {
    const item = { title: "", modal: !this.state.modal };
    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  editItem = item => {
    this.setState({ actiactiveItem: item, modal: !this.state.modal});
  };

  displayCompleted = status => {
    if (status) {
      return this.setState({ viewCompleted: true });
    }
    return this.setState({ viewCompleted: false });
  };

  renderTabList = () => {
    return (
      <div className="my-5 tab-list">
        <span
          onClick={() => this.displayCompleted(true)}
          className={this.state.viewCompleted ? "active" : ""}
        >
          Completed
        </span>
        <span
          onClick={() => this.displayCompleted(false)}
          className={this.state.viewCompleted ? "" : "active"}
        >
          Incomplete
        </span>
      </div>
    );
  }
// Rendering items in the list (completed || incomplete)
  renderItems = () => {
    const { viewCompleted } = this.state;
    const newItems = this.state.todoList.filter(
      item => item.completed == viewCompleted
    );

    return newItems.map(item => (
      <li 
      key={item.id}
      className="list-group-item d-flex justify-content-between align-items-center">
        <span className={`todo-title mr-2 ${this.state.viewCompleted ? "completed-todo" : ""}`}
        title={item.title}>
          {item.title}
        </span>
        <span>
          <button className="btn btn-info m-2">Edit</button>
          <button className="btn btn-danger m-2">Delete</button>
        </span>
      </li>
    )
    );
  }

render() {
  return(
    <main className='content p-3 mb-2 bg-info'>
      <h1 className='text-white text-uppercase text-center my-4'> Task Manager </h1>
      <div className="row">
        <div className="col-md-6 col-sma-10 mx-auto p-0">
          <div className='card p-3'>
            <div>
              <button className='btn btn-warning'>Add Task</button>
            </div>
            {this.renderTabList()}
            <ul className='list-group list-group-flush'>
              {this.renderItems()}
            </ul>
          </div>
        </div>
      </div>
      <footer className="my-3 mb-2 bg-info text-white text-center">Copyright 2023 &copy; All Rights Reserved</footer>
    {this.state.modal ? (
      <Modal activeItem={this.state.activeItem} toggle={this.toggle} onSave={this.handleSubmit} />
    ) : null}
    </main>
  );
}





}



export default App;
