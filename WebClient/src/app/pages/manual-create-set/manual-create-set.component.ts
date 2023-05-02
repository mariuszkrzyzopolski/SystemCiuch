import { Component } from '@angular/core';
import { DTOCollectionItemDetails } from 'src/app/model/DTOCollection';
import { CollectionService } from 'src/app/services/CollectionService';

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

  constructor(private collectionService: CollectionService) { }
  
  ngOnInit(): void {
    this.loadItems();
  }

  loadItems() {
    this.collectionService.getCollection().subscribe(data => {
      this.items = data.Collection.items;
      this.upperGarments = this.items.filter(item => item.type === 'Upper garment');
      this.lowerGarments = this.items.filter(item => item.type === 'Lower garment');
      this.footwear = this.items.filter(item => item.type === 'Footwear');
    });
  }
}
