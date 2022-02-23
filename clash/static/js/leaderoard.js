// $(function(){

//     var page =1, pagelimit=10, totalRecord=0, html;
//     fetchdata();
//     $(".prev-btn").on("click",function(){
//         if(page > 1)
//         {
//             page--;
//         }
//     });
//     $(".next-btn").on("click",function(){
//         if(ceil(page * pagelimit) < totalRecord)
//         {
//             page++;
//         }
//     });    
//     function fetchdata()
//     {
//         $.ajax
//         {
//             url:'http://localhost/credenz/leaderboard',
//             // url:'http://127.0.0.1:8000/credenz/leaderboard',
//             type:'GET',
//             data:{page:1,
//                 pagelimit:1},
//             success: function(data){
//                 console.log(data);
//                 for(var i=0;i<data.length;i++)
//                 {
//                     html += "<td>"+ data.counter +"</td>"+ "<td>" +data.username;
//                 }
//                 $("#result").html(html;)
//             },
//             error: function(jqXHR, textStatus, errorThrown)
//             {
//                 console.log(jqXHR);
//                 console.log(textStatus);
//                 console.log(errorThrown);
//             }
//         }
//     };


// });



// $(document).ready(function(){
//     load_data(10);
//     function load_data(page)
//     {
//         $.ajax
//         ({
//             url:'http://127.0.0.1:8000/credenz/leaderboard',
//             method:'POST',
//             data:{page:page},
//             success:function(data)
//             {
//                 $('#pagination_data').html(data); 
//             }
//         })
//     }
// });




// function loadcontent(){
//     $(document).ready(function(){
//         $.ajax({
//             type : 'POST',
//             url : "{%url 'clash-mysub' ques.id%}",
//             data: formdata,
//             success: function(response,res1){
//               console.log("bkc");
              
//               // console.log(response.opt);
//               // console.log(res1);
//               // console.log(res2);
//               $("#output").val(response.opt);
//             }
//           })
//     }
// }

function loadcontent(){
    
    $.ajax({
        type : 'POST',
        url : "{%url 'clash-mysub'}",
        success: function(response,res1,list){
          console.log("bkc");
          
          // console.log(response.opt);
          // console.log(res1);
          // console.log(res2);
          console.log(response.list);
          console.log(res1);
          console.log(list);
          
        //   $("#output").val(response.list);
        }
    })
}