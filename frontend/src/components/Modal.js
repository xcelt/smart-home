import React, { Component } from 'react'

import {
    Button,
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Form,
    FormGroup,
    Input,
    Label,
} from 'reactstrap';

class CustomModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            activeItem: this.props.activeItem
        };
    }

    handleChange = e => {
        let  { name, value } = e.target; 
        if (e.target.type === "checkbox") {
            value = e.target.checked;
        }
        const activeItem = {...this.state.activeItem, [name]: value };
        this.setState({ activeItem })
    };

    render() {
        const { toggle, onSave } = this.props;
        return(
            <Modal isOpen={true} toggle={toggle} >
                <ModalHeader>
                    Temperature Settings
                </ModalHeader>
                <ModalBody>
                    <Form>
                        <FormGroup>
                            {/* Living Room */}
                            <Label for="livingroom">Living Room</Label>
                            <Input
                            type="text"
                            name="Name"
                            value={this.state.activatedDevice.name}
                            onChange={this.handleChange}
                            placeholder="Set temperature for the living room:"
                            />
                        </FormGroup>
                    </Form>
                </ModalBody>
                <ModalFooter>
                    <Button color="info" onClick={() => onSave(this.state.activeItem)}>
                        Save
                    </Button>
                </ModalFooter>
            </Modal>
        )
    }
}

export default CustomModal

