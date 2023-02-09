import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AddClothes } from '../../model/AddClothes';

@Component({
  selector: 'app-add-clothes',
  templateUrl: './add-clothes.component.html',
  styleUrls: ['./add-clothes.component.css']
})
export class AddClothesComponent implements OnInit {

  type = ['Góra', 'Dół', 'Buty'];
  addclothesForm: FormGroup;

  ngOnInit() {
    this.addclothesForm = new FormGroup({
      'type': new FormControl('Góra'),
      'formGroupData': new FormGroup({
        'tags': new FormControl(null, Validators.required),
        'description': new FormControl(null, Validators.required)
      })
    });
  }

  onSubmit() {

    var formGroupData = this.addclothesForm.value.formGroupData;

    var addclothesFormData = {
      tags: formGroupData.tags,
      description: formGroupData.description,
      type: this.addclothesForm.value.type
    } as AddClothes;

    console.log(addclothesFormData);
  }
}
