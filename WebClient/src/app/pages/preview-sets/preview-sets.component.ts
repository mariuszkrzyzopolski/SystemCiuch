import { Component } from '@angular/core';
import { SetService } from 'src/app/services/SetService';

@Component({
  selector: 'app-preview-sets-component',
  templateUrl: './preview-sets.component.html',
  styleUrls: ['./preview-sets.component.css']
})
export class PreviewSetsComponent {
  sets: any[];
  showModal = false;
  setId: number | null = null;
  constructor(private setService: SetService) { }

  ngOnInit(): void {
    this.loadData();
  }

  removeSet(setId: number) {
    this.setId = setId;
    this.showModal = true;
  }

  confirmRemoveSet() {
    if(!this.setId) {
      return;
    }

    this.setService.deleteSet(this.setId).subscribe(
      response => {
        this.loadData();
        this.showModal = false;
      },
      error => {
        console.error(error);
      }
    );
  }
  loadData(){
    this.setService.getSets().subscribe(
      response => {
        this.sets = response;
      },
      error => {
        console.error(error);
      }
    );
  }
}
