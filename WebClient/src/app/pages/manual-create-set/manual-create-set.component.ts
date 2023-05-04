import { Component } from '@angular/core';
import { DTOCollectionItemDetails } from 'src/app/model/DTOCollection';
import { SliderChange } from 'src/app/model/SliderChange';
import { CollectionService } from 'src/app/services/CollectionService';
import { SetService } from 'src/app/services/SetService';

@Component({
  selector: 'app-manual-create-set',
  templateUrl: './manual-create-set.component.html',
  styleUrls: ['./manual-create-set.component.css']
})
export class ManualCreateSetComponent {
  items: DTOCollectionItemDetails[];
  upperGarments: DTOCollectionItemDetails[];
  lowerGarments: DTOCollectionItemDetails[];
  footwear: DTOCollectionItemDetails[];
  detailsItem: DTOCollectionItemDetails | null = null;
  itemToRemove: DTOCollectionItemDetails | null = null;
  showModal = false;
  showDetailsModal = false;
  editDetails = false;
  first_item_id: number | null = null;
  second_item_id: number | null = null;
  third_item_id: number | null = null;
  
  constructor(private collectionService: CollectionService, private setService: SetService) { }
  
  ngOnInit(): void {
    this.loadItems();
  }

  loadItems() {
    this.collectionService.getCollection().subscribe(data => {
      this.items = data.Collection.items;
      this.upperGarments = this.items.filter(item => item.type === 'Upper garment');
      this.lowerGarments = this.items.filter(item => item.type === 'Lower garment');
      this.footwear = this.items.filter(item => item.type === 'Footwear');

      if(this.upperGarments.length > 2 && this.lowerGarments.length > 2 && this.footwear.length > 2) {
        this.first_item_id = this.upperGarments[1].id;
        this.second_item_id = this.lowerGarments[1].id;
        this.third_item_id = this.footwear[1].id;
      }
      
    });
  }

  saveSet(){
    this.setService.addSet(this.first_item_id!, this.second_item_id!, this.third_item_id!).subscribe(data => {
      this.showModal = true;
    })
  }

  changeSlide(change: SliderChange) {
    if(change.type == 'Góra') {
      this.first_item_id = change.currentId;
    } else if (change.type == 'Dół') {
      this.second_item_id = change.currentId;
    }
    else if (change.type == 'Obuwie') {
      this.third_item_id = change.currentId;
    }
  }
}
