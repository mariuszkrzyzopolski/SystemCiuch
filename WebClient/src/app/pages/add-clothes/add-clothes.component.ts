import { Component, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-add-clothes',
  templateUrl: './add-clothes.component.html',
  styleUrls: ['./add-clothes.component.css']
})
export class AddClothesComponent {
  @ViewChild('f') addclothesForm: NgForm;
  defaultType='Góra';

// onSubmit(form:NgForm){
//   console.log(form);
// }
onSubmit(){
console.log(this.addclothesForm);
}
}
