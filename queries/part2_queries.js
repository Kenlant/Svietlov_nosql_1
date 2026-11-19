db = db.getSiblingDB("spotify");

{
  const filter = {
    "audio_features.danceability": { $gt: 0.7 },
    "audio_features.energy": { $gt: 0.7 },
    duration_ms: { $gte: 180000, $lte: 300000 }
  };
  const projection = {
    _id: 0,
    track_name: 1,
    artists: 1,
    track_genre: 1,
    popularity: 1,
    duration_ms: 1,
    "audio_features.danceability": 1,
    "audio_features.energy": 1
  };
  db.tracks.find(filter, projection);
}

{
  const pipeline = [
    { $unwind: "$artists" },
    { $group: { _id: { artist: "$artists", track_id: "$track_id" }, popularity: { $max: "$popularity" } } },
    { $group: { _id: "$_id.artist", track_count: { $sum: 1 }, min_popularity: { $min: "$popularity" }, avg_popularity: { $avg: "$popularity" } } },
    { $match: { track_count: { $gte: 3 }, min_popularity: { $gte: 60 } } },
    { $sort: { avg_popularity: -1, track_count: -1, _id: 1 } },
    { $limit: 20 },
    { $project: { _id: 0, artist: "$_id", track_count: "$track_count", min_popularity: { $round: ["$min_popularity", 1] }, avg_popularity: { $round: ["$avg_popularity", 1] } } }
  ];
  printjson(db.tracks.aggregate(pipeline).toArray());
}

{
  const pipeline = [
    { $group: { _id: "$track_genre", avg_tempo: { $avg: "$audio_features.tempo" }, std_tempo: { $stdDevPop: "$audio_features.tempo" } } },
    { $addFields: { outlier_threshold: { $add: ["$avg_tempo", { $multiply: [2, "$std_tempo"] }] } } },
    {
      $lookup: {
        from: "tracks",
        localField: "_id",
        foreignField: "track_genre",
        let: { threshold: "$outlier_threshold" },
        pipeline: [
          { $match: { $expr: { $gt: ["$audio_features.tempo", "$$threshold"] } } },
          { $sort: { "audio_features.tempo": -1 } },
          { $project: { track_name: 1, popularity: 1, artists: 1, "audio_features.tempo": 1 } }
        ],
        as: "outlier_tracks"
      }
    },
    { $project: { _id: 0, avg_tempo: { $round: ["$avg_tempo", 1] }, genre: "$_id", outlier_threshold: { $round: ["$outlier_threshold", 1] }, outlier_tracks: "$outlier_tracks" } },
    { $sort: { genre: 1 } }
  ];
  db.tracks.aggregate(pipeline);
}

{
  const filter = {
    "audio_features.loudness": { $lt: -10 },
    "audio_features.speechiness": { $lt: 0.1 },
    "audio_features.instrumentalness": { $gt: 0.5 },
    explicit: false
  };
  const projection = { _id: 0, track_name: 1, artists: 1, track_genre: 1, popularity: 1, explicit: 1, "audio_features.loudness": 1, "audio_features.speechiness": 1, "audio_features.instrumentalness": 1 };
  db.tracks.find(filter, projection);
}
