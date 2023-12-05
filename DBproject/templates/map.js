// map.js
document.addEventListener("DOMContentLoaded", function () {
    // URL에서 검색어 가져오기
    var urlParams = new URLSearchParams(window.location.search);
    var searchTerm = urlParams.get('searchTerm');

    // 검색어가 있을 경우에만 지도 생성
    if (searchTerm) {
        var mapContainer = document.getElementById('mapContainer'),
            mapOption = {
                center: new kakao.maps.LatLng(33.450701, 126.570667),
                level: 3
            };
        var map = new kakao.maps.Map(mapContainer, mapOption);
        // 검색어를 활용하여 주소를 좌표로 변환
        addr_to_lat_lon(searchTerm, function (result) {
            // var markerPosition = new kakao.maps.LatLng(result[1], result[0]);
            var markerPosition = new kakao.maps.LatLng(lat, lon);
            
            // 마커 이미지 URL 또는 기본 마커 이미지를 사용할 경우 생략 가능
            var markerImage = new kakao.maps.MarkerImage(
                "./static/hospital.png", // 마커 이미지 URL
                new kakao.maps.Size(50, 50)
            ); // 마커 이미지 크기

            var marker = new kakao.maps.Marker({
                position: markerPosition,
                image: markerImage, // 마커 이미지 설정
            }); 

        // 마커 지도에 표시
        marker.setMap(map);
        // 지도 중심을 마커 위치로 이동
        map.setCenter(markerPosition);
        });
    }
});

function addr_to_lat_lon(addr, callback) {
    var url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + encodeURIComponent(addr);
    var headers = { "Authorization": "key를 입력하시오." };

    // 주소 → 좌표 변환 API 호출
    fetch(url, { headers: headers })
        .then(response => response.json())
        .then(data => {
            if (data.documents.length > 0) {
                var match_first = data.documents[0];
                callback([parseFloat(match_first.x), parseFloat(match_first.y)]);
            } else {
                console.error('No result found for the address:', addr);
            }
        })
        .catch(error => console.error('Error during address to coordinate conversion:', error));
}
