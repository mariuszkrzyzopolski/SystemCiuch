import { Component} from '@angular/core';
;
import SwiperCore, { Navigation, Pagination, Scrollbar, A11y } from 'swiper';
SwiperCore.use([Navigation, Pagination, Scrollbar, A11y]);

@Component({
  selector: 'app-clothes-prviev',
  templateUrl: './clothes-preview.component.html',
  styleUrls: ['./clothes-preview.component.css'],
})
export class ClothesPreviewComponent {

}


