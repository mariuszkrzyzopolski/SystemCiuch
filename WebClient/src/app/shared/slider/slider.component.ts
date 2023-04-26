import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DTOCollectionItemDetails } from '../../../app/model/CollectionDTO';
import { SwiperOptions } from 'swiper';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent {
  @Input() clothType: string;
  @Input() items: DTOCollectionItemDetails[];
  @Output() showDetailsEvent = new EventEmitter<DTOCollectionItemDetails>();
  
  config: SwiperOptions = {
    slidesPerView: 3,
    spaceBetween: 50,
    navigation: true,
    pagination: { clickable: true },
    scrollbar: { draggable: true },
  };
  onSwiper([swiper]: any) {
    console.log(swiper);
  }
  onSlideChange() {
    console.log('slide change');
  }

  showDetails(item: DTOCollectionItemDetails) {
    this.showDetailsEvent.emit(item);
  }
}
