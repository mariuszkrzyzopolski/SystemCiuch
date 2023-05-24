import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AddClothes } from '../../model/AddClothes';

@Component({
  selector: 'app-add-clothes',
  templateUrl: './add-clothes.component.html',
  styleUrls: ['./add-clothes.component.css']
})
export class AddClothesComponent implements OnInit {
  
  fielesToUpload: File[] = [];

  constructor(private http: HttpClient) { }

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
      tags: formGroupData.tags.split(','),
      description: formGroupData.description,
      type: this.addclothesForm.value.type,
      image: this.fielesToUpload[0]
    } as AddClothes;
    
    this.submitForm(addclothesFormData);
  }

  submitForm(addClothes: AddClothes){
    var formData: any = new FormData();
    formData.append("tags", addClothes.tags);
    formData.append("description", addClothes.description);
    formData.append("type", this.mapTypeToDto(addClothes.type));
    formData.append("image", addClothes.image);

    this.http.post('http://127.0.0.1:8000/collection/item', formData).subscribe(
      (response) => console.log(response),
      (error) => console.log(error)
    )
  }
  mapTypeToDto(type: string): any {
    switch (type) {
      case 'Góra':
        return 'Upper garment';
      case 'Dół':
        return 'Lower garment';
      case 'Buty':
        return 'Footwear'
      default:
        console.log(`Niepoprawny typ ubrania ${type}.`);
    }
  }

  onDragOver(event: any) {
    event.preventDefault();
  }

  onDropSuccess(event: any) {
      event.preventDefault();
      this.onFileChange(event.dataTransfer.files);    
  }

  onChange(event: any) {
    this.onFileChange(event.target.files);   
  }

  private onFileChange(files: File[]) {
    this.fielesToUpload = files;
  }
}
