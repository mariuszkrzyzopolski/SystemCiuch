import { Component, OnInit} from '@angular/core';
import { DTOCollectionItem, DTOCollectionItemDetails } from '../../model/DTOCollection';
;
import SwiperCore, { Navigation, Pagination, Scrollbar, A11y } from 'swiper';
import { CollectionService } from '../../../app/services/CollectionService';
import { ItemTags } from 'src/app/model/ItemTags';
SwiperCore.use([Navigation, Pagination, Scrollbar, A11y]);

@Component({
  selector: 'app-clothes-prviev',
  templateUrl: './clothes-preview.component.html',
  styleUrls: ['./clothes-preview.component.css'],
})
export class ClothesPreviewComponent implements OnInit {
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
  showSettings(item: DTOCollectionItemDetails) {
    this.showDetailsModal = true;
    this.editDetails = true;
    this.detailsItem = item;
  }

  cancelDetails(){
    this.showDetailsModal = false;
  }

  showDetails(item: DTOCollectionItemDetails) {
     this.showDetailsModal = true;
     this.editDetails = false;
     this.detailsItem = item;
  }

  delete(item: DTOCollectionItemDetails) {
    this.itemToRemove = item;
    this.showModal = true;
  }

  cancelRemove() {
    this.showModal = false;
  }
  
  save(tags: ItemTags) {
    this.collectionService.save(tags.id, tags.tags).subscribe(data =>  {
      this.showDetailsModal = false;
      this.loadItems();
    });
  }

  removeItem(){
    this.collectionService.deleteCollectionItem(this.itemToRemove!.id).subscribe(data =>  {
      this.showModal = false;
      this.loadItems();
    });
  }
}


